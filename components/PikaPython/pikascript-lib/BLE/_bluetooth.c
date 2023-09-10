#include "pikaScript.h"
#include "nimble/ble.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
// #include "nimble/host/include/host/ble_gap.h"
#include "host/ble_hs.h"
#include "host/util/util.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"
#include "services/ans/ble_svc_ans.h"

#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_log.h"
// #include "ble_uuid.h"
#include "cb_event_id.h"

// TODO:发布的时候怎么将printf隐藏掉
// #define printf __platform_printf
#define printf pika_platform_printf

#define GATT_SVR_SVC_ALERT_UUID               0x1811
// BLE_UUID_base = 0x00000000-0000-1000-8000-00805F9B34FB;
static const char *tag = "NimBLE_BLE";
bool BLE_ONLY = false;       //只使用BLE,默认否
bool BLE_FIRST_INIT = true;  //是否第一次初始化,默认是
// uint8_t own_addr_type;
PikaEventListener *g_pika_ble_listener = NULL; // 事件监听器

// 函数声明
// GATT 服务端回调函数
static int ble_gatt_svc_access_cb(uint16_t conn_handle, uint16_t attr_handle,struct ble_gatt_access_ctxt *ctxt, void *arg);
// GATT 客户端写回调函数
static int ble_gatt_client_write_cb(uint16_t conn_handle,
                       const struct ble_gatt_error *error,
                       struct ble_gatt_attr *attr,
                       void *arg);
// GATT 客户端读回调函数
static int ble_gatt_client_read_cb(uint16_t conn_handle,
                       const struct ble_gatt_error *error,
                       struct ble_gatt_attr *attr,
                       void *arg);

// GATT mtu_exchange回调函数
static int ble_gatt_mtu_exchange_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            uint16_t mtu, void *arg);

// GATT 查找所有服务回调函数
static int ble_gatt_disc_all_svcs_cb(uint16_t conn_handle,
                                 const struct ble_gatt_error *error,
                                 const struct ble_gatt_svc *service,
                                 void *arg);

// GATT 查找所有服务回调函数
static int ble_gatt_disc_svcs_by_uuid_cb(uint16_t conn_handle,
                                 const struct ble_gatt_error *error,
                                 const struct ble_gatt_svc *service,
                                 void *arg);

// GATT 查找所有特性回调函数
static int ble_gatt_disc_all_chrs_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            const struct ble_gatt_chr *chr, void *arg);

// GATT 查找特定UUID特性回调函数
static int ble_gatt_disc_chrs_by_uuid_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            const struct ble_gatt_chr *chr, void *arg);

// GATT 查找所有描述符回调函数
static int ble_gatt_disc_all_dscs_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            uint16_t chr_val_handle,
                            const struct ble_gatt_dsc *dsc,
                            void *arg);

// GAP层回调函数
static int ble_gap_event_cb(struct ble_gap_event *event, void *arg);


// gatt初始化基本服务
void gatt_svr_init(void);

//
int read_uuid_from_str(char* buf, int len, ble_uuid_any_t* uuid_struct);

static const ble_uuid128_t gatt_svr_svc_uuid =
    BLE_UUID128_INIT(0x2d, 0x71, 0xa2, 0x59, 0xb4, 0x58, 0xc8, 0x12,
                     0x99, 0x99, 0x43, 0x95, 0x12, 0x2f, 0x46, 0x59);

/* A characteristic that can be subscribed to */
static uint8_t gatt_svr_chr_val;
static uint16_t gatt_svr_chr_val_handle;
static const ble_uuid128_t gatt_svr_chr_uuid =
    BLE_UUID128_INIT(0x00, 0x00, 0x00, 0x00, 0x11, 0x11, 0x11, 0x11,
                     0x22, 0x22, 0x22, 0x22, 0x33, 0x33, 0x33, 0x33);

/* A custom descriptor */
static uint8_t gatt_svr_dsc_val;
static const ble_uuid128_t gatt_svr_dsc_uuid =
    BLE_UUID128_INIT(0x01, 0x01, 0x01, 0x01, 0x12, 0x12, 0x12, 0x12,
                     0x23, 0x23, 0x23, 0x23, 0x34, 0x34, 0x34, 0x34);

static const struct ble_gatt_svc_def gatt_svr_svcs[] = {
    {
        /*** Service ***/
        .type = BLE_GATT_SVC_TYPE_PRIMARY,
        .uuid = &gatt_svr_svc_uuid.u,
        .characteristics = (struct ble_gatt_chr_def[])
        { {
                /*** This characteristic can be subscribed to by writing 0x00 and 0x01 to the CCCD ***/
                .uuid = &gatt_svr_chr_uuid.u,
                .access_cb = ble_gatt_svc_access_cb,
                .flags = BLE_GATT_CHR_F_READ | BLE_GATT_CHR_F_WRITE | BLE_GATT_CHR_F_NOTIFY | BLE_GATT_CHR_F_INDICATE,
                .val_handle = &gatt_svr_chr_val_handle,
                .descriptors = (struct ble_gatt_dsc_def[])
                { 
                    {
                      .uuid = &gatt_svr_dsc_uuid.u,
                      .att_flags = BLE_ATT_F_READ,
                      .access_cb = ble_gatt_svc_access_cb,
                    }, 
                    {
                      0, /* No more descriptors in this characteristic */
                    }
                },
            }, {
                0, /* No more characteristics in this service. */
            }
        },
    },

    {
        0, /* No more services. */
    },
};

// 蓝牙任务
void ble_host_task(void *param)
{
    ESP_LOGI(tag, "BLE Host Task Started");
    /* This function will return only when nimble_port_stop() is executed */
    nimble_port_run();
    nimble_port_freertos_deinit();
}

// 获取地址类型
uint8_t get_addr_type(int addr_mode)
{
    uint8_t own_addr_type;
    switch (addr_mode) {
        case 0:
            own_addr_type = BLE_OWN_ADDR_PUBLIC;
            break;
        case 1:
            own_addr_type = BLE_OWN_ADDR_RANDOM;
            break;
        case 2:
            own_addr_type = BLE_OWN_ADDR_RPA_PUBLIC_DEFAULT;
            break;
        case 3:
            own_addr_type = BLE_OWN_ADDR_RPA_RANDOM_DEFAULT;
            break;
    }
    return own_addr_type;
}

// int _bluetooth_BLE_init(PikaObj *self)
int _bluetooth_BLE_init(PikaObj *self)
{
    printf("_bluetooth_BLE___init__\r\n");
    if (BLE_FIRST_INIT)
    {
        //初始化flash
        esp_err_t ret = nvs_flash_init();
        if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
            ESP_ERROR_CHECK(nvs_flash_erase());
            ret = nvs_flash_init();
        }
        ESP_ERROR_CHECK(ret);
        BLE_FIRST_INIT = false;
    }
    return 1;
}

pika_bool _bluetooth_BLE_pyi_active(PikaObj *self, pika_bool active)
{
    printf("_bluetooth_BLE_pyi_active\r\n");
    if(active == true){
        //开始任务
        // nimble_port_freertos_init(ble_host_task);
        // 初始化堆栈
        // TODO: 多蓝牙对象时会报错
        nimble_port_init();
        // nimble_port_freertos_init(ble_host_task);
        return true;
    }else {
        nimble_port_deinit();
        // nimble_port_stop();
        return false;
    }
}

pika_bool _bluetooth_BLE_pyi_check_active(PikaObj *self)
{
    printf("_bluetooth_BLE_pyi_check_active\r\n");
    //TODO: 未找到检测蓝牙是否活跃的函数
    return true;
}

int _bluetooth_BLE_pyi_test(PikaObj *self)
{
    printf("_bluetooth_BLE_test\r\n");
    return 1;
}

void addr_inver(const void *addr,uint8_t *addr_inver)
{
    const uint8_t *u8p;
    u8p = addr;
    for ( int i = 0; i < 6; i++)
    {
        addr_inver[i] =  u8p[5-i];
    }

    // sprintf((char*)addr_inver,"%d%d%d%d%d%d",u8p[5],u8p[4],u8p[3],u8p[2],u8p[1],u8p[0]);
}

void print_addr(const void *addr)
{
    const uint8_t *u8p;
    u8p = addr;
    printf("%02x:%02x:%02x:%02x:%02x:%02x\r\n",u8p[5], u8p[4], u8p[3], u8p[2], u8p[1], u8p[0]);
}

/**
 * Logs information about a connection to the console.
 */
static void print_conn_desc(struct ble_gap_conn_desc *desc)
{
    MODLOG_DFLT(INFO, "handle=%d our_ota_addr_type=%d our_ota_addr=",
                desc->conn_handle, desc->our_ota_addr.type);
    print_addr(desc->our_ota_addr.val);
    MODLOG_DFLT(INFO, " our_id_addr_type=%d our_id_addr=",
                desc->our_id_addr.type);
    print_addr(desc->our_id_addr.val);
    MODLOG_DFLT(INFO, " peer_ota_addr_type=%d peer_ota_addr=",
                desc->peer_ota_addr.type);
    print_addr(desc->peer_ota_addr.val);
    MODLOG_DFLT(INFO, " peer_id_addr_type=%d peer_id_addr=",
                desc->peer_id_addr.type);
    print_addr(desc->peer_id_addr.val);
    MODLOG_DFLT(INFO, " conn_itvl=%d conn_latency=%d supervision_timeout=%d "
                "encrypted=%d authenticated=%d bonded=%d\r\n",
                desc->conn_itvl, desc->conn_latency,
                desc->supervision_timeout,
                desc->sec_state.encrypted,
                desc->sec_state.authenticated,
                desc->sec_state.bonded);
}

int _bluetooth_BLE_advertise(PikaObj *self, int addr, int interval, pika_bool connectable, 
        char* adv_data, int adv_data_len, char* rsp_data, int rsp_data_len)
{
    nimble_port_freertos_init(ble_host_task);
    printf("_bluetooth_BLE_gap_advertise\r\n");
    //  声明并初始化广播结构体
    struct ble_hs_adv_fields fields;
    memset(&fields, 0, sizeof fields);

    if(BLE_ONLY  == true){
        fields.flags |= BLE_HS_ADV_F_BREDR_UNSUP;
    }
    
    fields.tx_pwr_lvl_is_present = 1;
    fields.tx_pwr_lvl = BLE_HS_ADV_TX_PWR_LVL_AUTO;

    char* name = ble_svc_gap_device_name();
    fields.name = (uint8_t *)name;
    fields.name_len = strlen(name);
    fields.name_is_complete = 1;

    // TODO:UUID修改成可变的
    fields.uuids16 = (ble_uuid16_t[]) {
        BLE_UUID16_INIT(GATT_SVR_SVC_ALERT_UUID)
    };
    fields.num_uuids16 = 1;
    fields.uuids16_is_complete = 1;

    if(adv_data_len > 0)
    {
        fields.mfg_data = (uint8_t *)adv_data;
        fields.mfg_data_len = adv_data_len;
    }

    int rc = ble_gap_adv_set_fields(&fields);
    
    if (rc != 0) {
        MODLOG_DFLT(ERROR, "error setting advertisement data; rc=%d\n", rc);
        return -1 ;
    }

    //设置adv data
    // uint8_t* adv_data_new = (uint8_t*)malloc(adv_data_len + 2);
    // adv_data_new[0] = adv_data_len + 1;
    // adv_data_new[1] = 0xff;
    // memcpy(adv_data_new, adv_data+2, adv_data_len); 
    // rc =  ble_gap_adv_set_data(adv_data_new,adv_data_len+2);
    // if (rc != 0) {
    //     printf("error setting advertisement adv data; rc=%d\n", rc);
    //     free(adv_data_new);
    //     return -1 ;
    // }
    // free(adv_data_new);


    //设置rsp data
    if(rsp_data_len > 0) {
        uint8_t* rsp_data_new = (uint8_t*)malloc(rsp_data_len + 2);
        rsp_data_new[0] = rsp_data_len + 1;
        rsp_data_new[1] = 0xff;
        memcpy(rsp_data_new + 2, rsp_data, rsp_data_len); 
        rc =  ble_gap_adv_rsp_set_data(rsp_data_new,rsp_data_len+2);
        if (rc != 0) {
            printf("error setting advertisement response data; rc=%d\n", rc);
            free(rsp_data_new);
            return -1 ;
        }
        free(rsp_data_new);
    }


    // 声明并初始化广播结构体
    struct ble_gap_adv_params adv_params;
    memset(&adv_params, 0, sizeof(adv_params));

    // 获取地址类型
    uint8_t own_addr_type =  get_addr_type(addr);
    
    // 连接模式
    uint8_t connet_mode;
    if(connectable == true){
        connet_mode = BLE_GAP_CONN_MODE_UND;
    }else {
        connet_mode = BLE_GAP_CONN_MODE_NON;
    }

    adv_params.conn_mode = connet_mode;
    adv_params.disc_mode = BLE_GAP_DISC_MODE_GEN;
    if (interval < 30){  //TODO:需要大于30
        adv_params.itvl_min = 0; 
        adv_params.itvl_max = 0; 
    }else{  
        printf("interval : %d\r\n",interval);
        adv_params.itvl_min = interval; 
        adv_params.itvl_max = interval + 1; //只能和adv_params.itvl_min差1
    }
    return ble_gap_adv_start(own_addr_type, NULL, BLE_HS_FOREVER, &adv_params, ble_gap_event_cb, NULL);;
}

// 停止广播
// TODO:未验证
int _bluetooth_BLE_stop_advertise(PikaObj *self)
{
    printf("_bluetooth_BLE_stop_advertise\r\n");
    return ble_gap_adv_stop();
}

int _bluetooth_BLE_pyi_gap_connect(PikaObj *self, uint8_t* peer_addr, int peer_addr_type, int scan_duration_ms)
{
    // nimble_port_freertos_init(ble_host_task);
    printf("_bluetooth_BLE_gap_connect\r\n");

    int rc = ble_gap_disc_active();
    if (rc != 0) {
        printf("Failed to cancel scan; rc=%d\n", rc);
        return rc;
    }
    // uint8_t own_addr_type = get_addr_type(addr_type);
    uint8_t own_addr_type ;
    rc = ble_hs_id_infer_auto(0, &own_addr_type);
    printf("own_addr_type = %d\r\n", own_addr_type);
    
    if (rc != 0) {
        MODLOG_DFLT(ERROR, "error determining address type; rc=%d\n", rc);
        return rc;
    }

    uint8_t peer_addr_value[6];
    ble_addr_t addr_peer = {
        .type = 0,
    };
    addr_inver(peer_addr,addr_peer.val);
    // 0x0c,0xae,0xb0,0xb6,0xaf,0xa5
    // addr_peer.val[0] = 0xa5;
    // addr_peer.val[1] = 0xaf;
    // addr_peer.val[2] = 0xb6;
    // addr_peer.val[3] = 0xb0;
    // addr_peer.val[4] = 0xae;
    // addr_peer.val[5] = 0x0c;
    return ble_gap_connect(own_addr_type,&addr_peer,scan_duration_ms,NULL,ble_gap_event_cb,NULL);
    // return 0;
}

int _bluetooth_BLE_pyi_gap_disconnect(PikaObj *self)
{
    printf("_bluetooth_BLE_gap_disconnect\r\n");
    // TODO:不太确定是否对应该函数 
    return ble_gap_conn_cancel();
}

int _bluetooth_BLE_gap_disc(PikaObj *self, int addr_mode, int duration_ms, int interval, int window, pika_bool active)
{
    nimble_port_freertos_init(ble_host_task);
    printf("_bluetooth_BLE_gap_disc\r\n");
    // 获取地址类型                                             
    uint8_t own_addr_type =  get_addr_type(addr_mode);
    // 声明并初始化结构体实例
    struct ble_gap_disc_params disc_params = {
        .itvl = interval,
        .window = window,
        .passive = ~active,
    };
    if (duration_ms == 0){
        return ble_gap_disc(own_addr_type, BLE_HS_FOREVER, &disc_params, ble_gap_event_cb, NULL);
    }else{
        return ble_gap_disc(own_addr_type, duration_ms, &disc_params, ble_gap_event_cb, NULL);
    }
    
}

// 停止扫描
// 不会引发扫描中止事件
int _bluetooth_BLE_gap_stop_disc(PikaObj *self)
{
    printf("_bluetooth_BLE_gap_stop_scan\r\n");
    return ble_gap_disc_cancel();
}

// 注册服务
// TODO:未验证
int _bluetooth_BLE_gatts_register_svcs(PikaObj *self, PikaObj* services_info)
{
    // nimble_port_stop();
    // printf("_bluetooth_BLE_gatts_register_svcs\r\n");
    // size_t service_count , chr_count, dsc_count;
    // uint8_t i,j,k;
    // uint8_t *chrs_count_per_service;
    // struct ble_gatt_svc_def* gatt_svr_svcs;
    // struct ble_gatt_chr_def* gatt_svr_chrs;
    // struct ble_gatt_dsc_def* gatt_svr_dscs;

    // service_count = pikaTuple_getSize(services_info);            //服务的个数,是不确定的
    // printf("services_info service_count = %d\r\n",service_count);

    // gatt_svr_svcs = (struct ble_gatt_svc_def*) malloc((service_count + 1) * sizeof(struct ble_gatt_svc_def)); //申请空间
    // chrs_count_per_service    = (uint8_t*) malloc((service_count + 1) * sizeof(uint8_t));

    // if(gatt_svr_svcs == NULL){
    //     printf("malloc svcs memory error\r\n");
    //     return -1;
    // }


    // for (i = 0;i < service_count;i++){                             //对于每个服务
    //     PikaObj* service = arg_getObj(pikaTuple_getArg(services_info, i)); //读取服务
    //     char* service_UUID = pikaTuple_getStr(service,0);         //获取服务的UUID

    //     PikaObj* chrs = arg_getObj(pikaTuple_getArg(service, 1));//读取属性合集
    //     chr_count = pikaTuple_getSize(chrs);                       // 属性的个数,是不确定的

    //     gatt_svr_chrs = (struct ble_gatt_chr_def*) malloc((chr_count  + 1)* sizeof(struct ble_gatt_chr_def)); //申请空间
    //     if(gatt_svr_chrs == NULL){
    //         printf("malloc chrs memory error\r\n");
    //         return -1;
    //     }    
    //     chrs_count_per_service[i] = chr_count;
    //     // int uuid_size = read_uuid_from_str(service_UUID,);
    //     // gatt_svr_svcs[0].uuid = BLE_UUID16_DECLARE(test);

    //     printf("service %d UUID %s chrs size %d \r\n",i,service_UUID,chr_count);
    //     for (j = 0;j < chr_count;j++){                           // 对于每个属性
    //         PikaObj* chr = arg_getObj(pikaTuple_getArg(chrs, j));//读取属性

    //         char * chr_UUID = pikaTuple_getStr(chr,0);           //属性FLAG    
    //         uint64_t chr_flags = pikaTuple_getInt(chr,1);
    //         PikaObj* dscs = arg_getObj(pikaTuple_getArg(chr, 2));// dscs = 描述符合集
    //         dsc_count = pikaTuple_getSize(dscs);                 //描述符的个数，是不确定的

    //         gatt_svr_dscs = (struct ble_gatt_dsc_def*) malloc((dsc_count + 1 )* sizeof(struct ble_gatt_dsc_def)); //申请空间
    //         if(gatt_svr_dscs == NULL){
    //             printf("malloc dscs memory error\r\n");
    //             return -1;
    //         }    
    //         printf("chr_UUID : %s chr_flags %d dscs size:%d\r\n",chr_UUID,chr_flags,dsc_count);
    //         for(k = 0;k < dsc_count;k++){                        //对于每个描述符
    //             PikaObj* dsc = arg_getObj(pikaTuple_getArg(dscs, k));
    //             char * dscs_UUID = pikaTuple_getInt(dsc, 0);
    //             uint16_t dscs_flags = pikaTuple_getInt(dsc, 1);
    //             printf("dsc_UUID : %s, dsc_flags : %d\r\n",dscs_UUID,dscs_flags);
    //         }
    //     }
    // }
    
    //注册基本服务
    gatt_svr_init(); 

    // 注册服务
    int rc = ble_gatts_count_cfg(gatt_svr_svcs);
    if (rc != 0) {
        return rc;
    }

    rc = ble_gatts_add_svcs(gatt_svr_svcs);
    if (rc != 0) {
        return rc;
    }

    // 释放内存空间的时候需要遍历结构体
    // for (i = 0;i < service_count; i++){  
    //     gatt_svr_chrs = gatt_svr_svcs[i].characteristics;
    //     chr_count = chrs_count_per_service[i];       //FIXME:修改一下获取特性数量的方法
    //     for (j = 0;j < chr_count; j++){
    //         gatt_svr_dscs = gatt_svr_chrs[j].descriptors;
    //         free(gatt_svr_dscs);
    //     } 
    //     free(gatt_svr_chrs);
    // }
    // free(gatt_svr_svcs);
    // nimble_port_freertos_init(ble_host_task);
    return 0;
}

// 设置广播数据
// 在设置前需要蓝牙协议栈处于同步状态, nimble_port_freertos_init(ble_host_task)
// 直接发送传入内容, 不按照规范补充格式
// 若要按规范补充则需要调用ble_gap_adv_set_fields(const struct ble_hs_adv_fields *rsp_fields)函数
int _bluetooth_BLE_set_adv_data(PikaObj *self, uint8_t* data, int data_len)
{
    printf("_bluetooth_BLE_set_adv_data\r\n");
    return ble_gap_adv_set_data(data,data_len);
}

// 设置扫描响应数据
// 在设置前需要蓝牙协议栈处于同步状态, nimble_port_freertos_init(ble_host_task)
// 直接发送传入内容, 不按照规范补充格式
// 若要按规范补充则需要调用ble_gap_adv_rsp_set_fields(const struct ble_hs_adv_fields *rsp_fields)函数
// int _bluetooth_BLE_set_rsp_data(PikaObj *self, char* data, int data_len)
int _bluetooth_BLE_set_rsp_data(PikaObj *self, uint8_t* data, int data_len)
{
    printf("_bluetooth_BLE_set_rsp_data\r\n");
    // printf("%hx %hx %hx %hx\r\n",data[0],data[1],data[2],data[3]);
    // printf("%d %d %d %d\r\n",data[0],data[1],data[2],data[3]);
    return  ble_gap_adv_rsp_set_data(data,data_len);
}


int _bluetooth_BLE_config_mac_get(PikaObj *self)
{
    printf("_bluetooth_BLE_config_mac_get\r\n");
    // uint8_t addr[6];
    // ble_addr_t baddr;
    
    // /* 获取设备的MAC地址 */
    // printf("nimble_port_get_addr result: %d",nimble_port_get_addr(&baddr));
    
    // /* 将地址拷贝到 addr 数组中 */
    // memcpy(addr, baddr.val, sizeof(addr));
    
    // /* 打印MAC地址 */
    // printf("Device MAC Address: %02x:%02x:%02x:%02x:%02x:%02x\n",
    //        addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]);

    return 0;
}


// 测试通过
char* _bluetooth_BLE_config_gap_name_get(PikaObj *self){
    printf("_bluetooth_BLE_config_addr_gap_name_get\r\n");
    char *name = ble_svc_gap_device_name();
    return obj_cacheStr(self, name);
}

int _bluetooth_BLE_config_addr_mode_get(PikaObj *self){
    printf("_bluetooth_BLE_config_addr_mode_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_mtu_get(PikaObj *self){
    printf("_bluetooth_BLE_config_mtu_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_addr_rxbuf_get(PikaObj *self){
    printf("_bluetooth_BLE_config_addr_rxbuf_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_bond_get(PikaObj *self){
    printf("_bluetooth_BLE_config_bond_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_io_get(PikaObj *self)
{
    printf("_bluetooth_BLE_config_io_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_le_secure_get(PikaObj *self)
{
    printf("_bluetooth_BLE_config_le_secure_get\r\n");
    return 0;
}

int _bluetooth_BLE_config_mitm_get(PikaObj *self)
{
    printf("_bluetooth_BLE_config_mitm_get\r\n");
    return 0;
}


int _bluetooth_BLE_config_addr_mode_update(PikaObj *self)
{
    printf("_bluetooth_BLE_config_addr_mode_update\r\n");
    return 0;
}

int _bluetooth_BLE_config_bond_update(PikaObj *self, pika_bool bond)
{
    printf("_bluetooth_BLE_config_bond_update\r\n");
    return 0;
}

// 基本测试通过
// TODO:gap_name输入的是其他格式呢?
int _bluetooth_BLE_config_gap_name_update(PikaObj *self, char* gap_name)
{
    printf("_bluetooth_BLE_config_gap_name_update\r\n");
    return ble_svc_gap_device_name_set(gap_name);
}

// TODO:未找到对应函数
int _bluetooth_BLE_config_io_update(PikaObj *self, int io){
    printf("_bluetooth_BLE_config_io_update\r\n");
    return 0;
}

int _bluetooth_BLE_config_le_secure_update(PikaObj *self, pika_bool le_secure)
{
    ESP_LOGD(tag, "_bluetooth_BLE_config_le_secure_update\r\n");
    // TODO:需要进行判断，若BLE处于广播状态则不能修改
    if(ble_gap_adv_active()){
        ESP_LOGI(tag, "an advertisement procedure is currently in progress\r\n");
        return -1;
    }
    else{
        BLE_ONLY = le_secure;
        ESP_LOGI(tag, "secure update succeed\r\n");
        return 0;
    }
}

// TODO:未找到实现方法
int _bluetooth_BLE_config_mac_update(PikaObj *self)
{
    printf("_bluetooth_BLE_config_mac_update\r\n");
    return 0;
}

// TODO:未找到对应函数
int _bluetooth_BLE_config_mitm_update(PikaObj *self, pika_bool mitm)
{
    printf("_bluetooth_BLE_config_mitm_update\r\n");
    return 0;
}

// TODO:未找到对应函数
int _bluetooth_BLE_config_mtu_update(PikaObj *self, int mtu)
{
    printf("_bluetooth_BLE_config_mtu_update\r\n");
    return 0;
}

// TODO:未找到对应函数
int _bluetooth_BLE_config_rxbuf_update(PikaObj *self, int rxbuf)
{
    printf("_bluetooth_BLE_config_rxbuf_update\r\n");
    return 0;
}


int _bluetooth_BLE_pyi_test2(PikaObj *self,char *data ,int data_len)
{
    // printf("_bluetooth_BLE_pyi_test2\r\n");
    // printf("%d\r\n",data[0]);
    // _testtest(num);
    // uint8_t* prt_num  = (uint8_t * )malloc(data_len);
    // // printf("%s\r\n",atoi(num));
    // for ( int i = 0; i < data_len; i++)
    // {
    //     prt_num[i] = data[i] - '0';
    //     // printf("%d",data[i]-48);
    // }
    
    // for ( int i = 0; i < data_len; i++)
    // {
    //     printf("%d",prt_num[i]);
    // }
    // printf("\r\n");
    // free(prt_num);

    // BLE_UUID16(uuid)->value;

    // unsigned int aa1, aa2, aa3,aa4;//注意不能用unsigned char
    // sscanf( data, "%02x%02x%02x%02x", &aa1, &aa2, &aa3 ,&aa4);
    // printf( "%02x,%02x,%02x,%02x\r\n", aa1, aa2, aa3 ,aa4);

    // printf("%s\r\n",data);
    // unsigned int aa1, aa2, aa3,aa4;
    // printf("%d\r\n",strlen(data));
    // sscanf(data,"%02x%02x%02x",&aa1,&aa2,&aa3);
    // printf("%d,%d,%d,%d\r\n",aa1,aa2,aa3);
    // printf("data len = %d\r\n",data_len);
    printf("data = %s\r\n",(uint8_t*)data);
    return 0;
}

int _bluetooth_BLE_pyi_test3(PikaObj *self)
{
    printf("_bluetooth_BLE_pyi_test3\r\n");
    ble_svc_gap_device_name_set("nimble-test");
    return 0;
}

int _bluetooth_BLE_test_call_some_name(PikaObj *self)
{
    printf("_bluetooth_BLE_test_call_some_name\r\n");
    return 0;
}

//通过UUID查找全部属性
//TODO:待验证
int _bluetooth_BLE_gattc_dis_chrs(PikaObj *self, int conn_handle, int start_handle, int end_handle){
    return ble_gattc_disc_all_chrs(conn_handle,start_handle,end_handle,ble_gatt_disc_all_chrs_cb,NULL);;
}

//通过UUID查找属性
//TODO:传入UUID的方法未找到，目前好像只是类型
int _bluetooth_BLE_gattc_dis_chrs_by_uuid(PikaObj *self, int conn_handle, int start_handle, int end_handle, char* uuid){
    ble_uuid_t * chr_uuid = BLE_UUID_TYPE_16;
    return ble_gattc_disc_chrs_by_uuid(conn_handle,start_handle,end_handle,chr_uuid,ble_gatt_disc_chrs_by_uuid_cb,NULL);
}

//查找全部描述符
//TODO:待验证
int _bluetooth_BLE_gattc_dis_dscs(PikaObj *self, int conn_handle, int start_handle, int end_handle){
    return ble_gattc_disc_all_dscs(conn_handle,start_handle,end_handle,ble_gattc_disc_all_dscs,NULL);
}

//查找全部服务
//TODO:待验证
int _bluetooth_BLE_gattc_dis_svcs(PikaObj *self, int conn_handle){
    return ble_gattc_disc_all_svcs(conn_handle, ble_gattc_disc_all_svcs, NULL);
}

//通过UUID查找服务
//TODO:传入UUID的方法未找到，目前好像只是类型
int _bluetooth_BLE_gattc_dis_svcs_by_uuid(PikaObj *self, int conn_handle, char* uuid){
    ble_uuid_t * svcs_uuid = BLE_UUID_TYPE_16;
    return ble_gattc_disc_svc_by_uuid(conn_handle, svcs_uuid,ble_gattc_disc_svc_by_uuid, NULL);
}

// GATT读属性、描述符
// TODO:未验证
int _bluetooth_BLE_pyi_gattc_read(PikaObj *self, int conn_handle, int value_handle){
    return ble_gattc_read(conn_handle, value_handle,ble_gatt_client_read_cb, NULL);
}

// GATT写属性、描述符
//TODO:还有一个相同功能的函数但不知道区别
// ble_gattc_write_no_rsp(uint16_t conn_handle, uint16_t attr_handle, struct os_mbuf *om)
int _bluetooth_BLE_gattc_write_with_no_rsp(PikaObj *self, int conn_handle, int value_handle, char* data, int data_len){
    return ble_gattc_write_no_rsp_flat(conn_handle,value_handle,data,data_len);
}

// GATT写属性、描述符
//TODO:还有一个相同功能的函数但不知道区别
// ble_gattc_write(uint16_t conn_handle, uint16_t attr_handle,struct os_mbuf *txom, ble_gatt_attr_fn *cb, void *cb_arg)
int _bluetooth_BLE_gattc_write_with_rsp(PikaObj *self, int conn_handle, int value_handle, char* data, int data_len){
    return ble_gattc_write_flat(conn_handle,value_handle,data,data_len,ble_gatt_client_write_cb,NULL);
}

// GATT indicate
// TODO:struct os_mbuf txom是个什么样的格式类型
int _bluetooth_BLE_gatts_indicate_custom(PikaObj *self, int conn_handle, int value_handle, char* data){
    struct os_mbuf txom = {
        .om_len = 2,
    };
    return ble_gatts_indicate_custom(conn_handle, value_handle, &txom);
}

// TODO:no data的话实际上传的是啥
int _bluetooth_BLE_gatts_indicate_no_data(PikaObj *self, int conn_handle, int value_handle){
    return ble_gatts_indicate(conn_handle, value_handle);
}

// TODO: struct os_mbuf ??
int _bluetooth_BLE_gatts_notify_custom(PikaObj *self, int conn_handle, int value_handle, char* data){
    struct os_mbuf om = {
        .om_len = 2,
    };
    return ble_gattc_notify_custom(conn_handle, value_handle, &om);
}

// TODO:no data的话实际上传的是啥
int _bluetooth_BLE_gatts_notify_no_data(PikaObj *self, int conn_handle, int value_handle){
    return ble_gatts_notify(conn_handle,value_handle);
}

// 未找到正确的使用方法与效果
// TODO:待验证
int _bluetooth_BLE_pyi_gattc_exchange_mtu(PikaObj *self, int conn_handle){
    return ble_gattc_exchange_mtu(conn_handle,ble_gatt_mtu_exchange_cb,NULL);
}


// 回调函数注册
void _bluetooth_BLE_setCallback(PikaObj *self, Arg* cb)
{
    printf("_bluetooth_BLE_setCallback\r\n");
    if (g_pika_ble_listener == NULL) {
        pika_eventListener_init(&g_pika_ble_listener);
        printf("g_pika_ble_listener init\r\n");
    }
    uint32_t i = 0;
    for ( i = 0; i < _IRQ_COUNT + 1; i++){
        pika_eventListener_registEventCallback(g_pika_ble_listener,i,cb);
    }
}

// 基本服务注册
void gatt_svr_init(void)
{
    ble_svc_gap_init();
    ble_svc_gatt_init();
    // ble_svc_ans_init();
}

// 从字符串中读取UUID 结构体
int read_uuid_from_str(char* buf, int len, ble_uuid_any_t* uuid_struct)
{
    unsigned int a[16];
    if (len == 4){
        sscanf(buf, "%02x%02x", &a[0],&a[1]);
        uuid_struct->u16.u.type = BLE_UUID_TYPE_16;
        uuid_struct->u16.value = (a[0] << 8) | a[1];
        return 16;
    }
    else if (len == 8){
        sscanf(buf, "%02x%02x%02x%02x", &a[0],&a[1],&a[2],&a[3]);
        uuid_struct->u32.u.type = BLE_UUID_TYPE_32;
        uuid_struct->u32.value  = (a[0] << 24) | (a[1] << 16) | (a[2] << 8) | a[3]; 
        return 32;
    }
    else if (len == 36){
        sscanf(buf, "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",\
         &a[15],&a[14],&a[13],&a[12],&a[11],&a[10],&a[9],&a[8],&a[7],&a[6],&a[5],&a[4],&a[3],&a[2],&a[1],&a[0]);
        // // &a[0],&a[1],&a[2],&a[3],&a[4],&a[5],&a[6],&a[7],&a[8],&a[9],&a[10],&a[11],&a[12],&a[13],&a[14],&a[15]);
        uuid_struct->u128.u.type = BLE_UUID_TYPE_128;
        memcpy(uuid_struct->u128.value,a,16);
        return 128;
    }
    return 0;
}


// GATT层:服务端回调函数
static int ble_gatt_svc_access_cb(uint16_t conn_handle, uint16_t attr_handle,
                struct ble_gatt_access_ctxt *ctxt, void *arg){
    const ble_uuid_t *uuid;
    int rc;
    switch (ctxt->op) {                       
        case BLE_GATT_ACCESS_OP_READ_CHR:       //读属性值
            if (conn_handle != BLE_HS_CONN_HANDLE_NONE) {
                printf("Characteristic read; conn_handle=%d attr_handle=%d\n",conn_handle, attr_handle);
                pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_READ_REQUEST,
                    arg_newObj(New_pikaTupleFrom(
                            arg_newInt(_IRQ_GATTS_READ_REQUEST),
                            arg_newInt(conn_handle),
                            arg_newInt(attr_handle)
                            )));
            } else {
                printf("Characteristic read by NimBLE stack; attr_handle=%d\n",attr_handle);
            }
            return 0;

        case BLE_GATT_ACCESS_OP_WRITE_CHR:     //写属性值
            if (conn_handle != BLE_HS_CONN_HANDLE_NONE) {
                printf("Characteristic write; conn_handle=%d attr_handle=%d", conn_handle, attr_handle);
                pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_WRITE,
                    arg_newObj(New_pikaTupleFrom(
                            arg_newInt(_IRQ_GATTS_WRITE),
                            arg_newInt(conn_handle),
                            arg_newInt(attr_handle)
                            )));
            } else {
                printf("Characteristic write by NimBLE stack; attr_handle=%d",attr_handle);
            }
            return 0;

        case BLE_GATT_ACCESS_OP_READ_DSC:     //读描述符(与属性值先不做区分)
            if (conn_handle != BLE_HS_CONN_HANDLE_NONE) {
                printf("Descriptor read; conn_handle=%d attr_handle=%d\r\n",conn_handle, attr_handle);
                pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_READ_REQUEST,
                    arg_newObj(New_pikaTupleFrom(
                            arg_newInt(_IRQ_GATTS_READ_REQUEST),
                            arg_newInt(conn_handle),
                            arg_newInt(attr_handle)
                            )));
            } else {
                printf("Descriptor read by NimBLE stack; attr_handle=%d\r\n",attr_handle);
            }
            return 0;

        case BLE_GATT_ACCESS_OP_WRITE_DSC:      //写描述符
            if (conn_handle != BLE_HS_CONN_HANDLE_NONE) {
                printf("Descriptor read; conn_handle=%d attr_handle=%d\r\n",conn_handle, attr_handle);
                pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_WRITE,
                    arg_newObj(New_pikaTupleFrom(
                            arg_newInt(_IRQ_GATTS_WRITE),
                            arg_newInt(conn_handle),
                            arg_newInt(attr_handle)
                            )));
            } else {
                printf("Descriptor read by NimBLE stack; attr_handle=%d\r\n",attr_handle);
            }
            return 0;
    }
    return 0;
}



// GATT层：客户端读服务回调函数
static int ble_gatt_client_read_cb(uint16_t conn_handle,
                       const struct ble_gatt_error *error,
                       struct ble_gatt_attr *attr,
                       void *arg)
{
    printf("Read complete for the subscribable characteristic; "
                "status=%d conn_handle=%d", error->status, conn_handle);

    //读取成功
    pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_READ_DONE ,
        arg_newObj(New_pikaTupleFrom(
                arg_newInt(_IRQ_GATTC_READ_DONE),
                arg_newInt(conn_handle),
                arg_newInt(attr->handle),
                arg_newInt(error->status) 
                )));

    if (error->status == 0) {
        printf(" attr_handle=%d value=", attr->handle);
        //读到数据
        pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_READ_RESULT,
            arg_newObj(New_pikaTupleFrom(
                    arg_newInt(_IRQ_GATTC_READ_RESULT),
                    arg_newInt(conn_handle),
                    arg_newInt(attr->handle),
                    arg_newStr("test string") //, 
                    // arg_newBytes(attr->om->om_databuf,attr->om->om_len) //TODO:未验证
                    )));
        // print_mbuf(attr->om); //TODO:该函数无引用，但在blecentn能够使用
    }
    return 0;
}

// GATT层：客户端写服务回调函数
static int ble_gatt_client_write_cb(uint16_t conn_handle,
                        const struct ble_gatt_error *error,
                        struct ble_gatt_attr *attr,
                        void *arg)
{
    const struct peer_chr *chr;
    const struct peer *peer;
    int rc;

    MODLOG_DFLT(INFO,
                "Write to the custom subscribable characteristic complete; "
                "status=%d conn_handle=%d attr_handle=%d\n",
                error->status, conn_handle, attr->handle);
        //读到数据
        pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_WRITE_DONE,
            arg_newObj(New_pikaTupleFrom(
                    arg_newInt(_IRQ_GATTC_WRITE_DONE ),
                    arg_newInt(conn_handle),
                    arg_newInt(attr->handle),
                    arg_newInt(error->status) 
                    )));
    return 0;
}

//GATT层 MTU exchange 回调函数
static int ble_gatt_mtu_exchange_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            uint16_t mtu, void *arg)
{
    if(error->status == 0){
        pika_eventListener_send(g_pika_ble_listener,_IRQ_MTU_EXCHANGED ,
        arg_newObj(New_pikaTupleFrom(
                arg_newInt(_IRQ_MTU_EXCHANGED),
                arg_newInt(conn_handle),
                arg_newInt(mtu)
                )));
    }
    return 0;
}


// GAP层：广播事件回调函数
static int ble_gap_event_cb(struct ble_gap_event *event, void *arg)
{
    struct ble_gap_conn_desc desc;
    int rc;
    uint8_t addr[6];

    switch (event->type) {
    case BLE_GAP_EVENT_CONNECT: //TODO:MicroPyhon 区分 服务端与客户端的连接
        /* A new connection was established or a connection attempt failed. */
        printf("connection %s; status=%d ",
            event->connect.status == 0 ? "established" : "failed", event->connect.status);
        printf("\r\n");
        if (event->connect.status == 0) {
            rc = ble_gap_conn_find(event->connect.conn_handle, &desc);
            assert(rc == 0);
            print_conn_desc(&desc);
            addr_inver(desc.peer_ota_addr.val,&addr);
            // char * test2 = "test2";
            // char * test3 = (char*)malloc(6);
            // test3[0] = 't';  
            // test3[1] = 'e';  
            // test3[2] = 's';  
            // test3[3] = 't';  
            // test3[4] = '3';  
            // test3[5] = '\0';  
            pika_eventListener_send(g_pika_ble_listener,_IRQ_CENTRAL_CONNECT,
                        arg_newObj(New_pikaTupleFrom(
                                arg_newInt(_IRQ_CENTRAL_CONNECT),
                                arg_newInt(event->connect.conn_handle),
                                arg_newInt(desc.peer_id_addr.type),
                                // arg_newStr("test"), //TODO:修改为arg_newBytes(desc.peer_ota_addr.val,6)
                                // arg_newStr(test2), 
                                // arg_newStr(test3), 
                                arg_newBytes(addr,6)
                                )));
            // free(test3);
        }

        if (event->connect.status != 0) {
            /* Connection failed; resume advertising. */
            // bleprph_advertise();
            // TODO: 重新广播
            printf("Connection failed; resume advertising.");
        }
        return 0;

    case BLE_GAP_EVENT_DISCONNECT: //断开连接
        printf("disconnect; reason=%d \r\n", event->disconnect.reason);
        print_conn_desc(&event->disconnect.conn);

        addr_inver(event->disconnect.conn.peer_ota_addr.val,&addr);
        pika_eventListener_send(g_pika_ble_listener,_IRQ_CENTRAL_DISCONNECT,
                            arg_newObj(New_pikaTupleFrom(
                                    arg_newInt(_IRQ_CENTRAL_DISCONNECT),
                                    arg_newInt(event->disconnect.conn.conn_handle),
                                    arg_newInt(desc.peer_id_addr.type),
                                    arg_newBytes(addr,6)
                                    )));
        return 0;

    case BLE_GAP_EVENT_CONN_UPDATE: //返回结果
        /* The central has updated the connection parameters. */
        printf("connection updated; status=%d \r\n",event->conn_update.status);
        rc = ble_gap_conn_find(event->conn_update.conn_handle, &desc);
        assert(rc == 0);
        print_conn_desc(&desc);
        return 0;

    case BLE_GAP_EVENT_CONN_UPDATE_REQ :
        // MicroPython : conn_handle, conn_interval, conn_latency, supervision_timeout, status 
        pika_eventListener_send(g_pika_ble_listener,_IRQ_CONNECTION_UPDATE,
                    arg_newObj(New_pikaTupleFrom(
                            arg_newInt(_IRQ_CONNECTION_UPDATE),
                            arg_newInt(event->conn_update_req.conn_handle),
                            arg_newInt(event->conn_update_req.peer_params->itvl_min),
                            arg_newInt(event->conn_update_req.peer_params->latency),
                            arg_newInt(event->conn_update_req.peer_params->supervision_timeout)//,
                            // arg_newInt(event->conn_update.status) TODO:status在上一事件中
                            )));
         return 0;

    case BLE_GAP_EVENT_L2CAP_UPDATE_REQ :
        return 0;

    case BLE_GAP_EVENT_TERM_FAILURE:
        
        return 0;
    
    case BLE_GAP_EVENT_DISC: //扫描发现
    // MicroPython addr_type, addr, adv_type, rssi, adv_data
        struct ble_gap_conn_desc desc;
        struct ble_hs_adv_fields fields;
        int rc;
        rc = ble_hs_adv_parse_fields(&fields, event->disc.data,event->disc.length_data);
        if (rc != 0) {
            return 0;
        }

        /* An advertisment report was received during GAP discovery. */
        // print_adv_fields(&fields);

        /* Try to connect to the advertiser if it looks interesting. */
        // blecent_connect_if_interesting(&event->disc);

        addr_inver(event->disc.addr.val,addr);
        // for (int i = 0; i < 6; i++)
        // {
        //     printf("%02x:", addr[i]);
        // }
        // printf("\r\n");
        // print_addr(event->disc.addr.val);
        // printf("length_data :%d \r\n",event->disc.length_data);

        // for (int i = 0; i < event->disc.length_data; i++)
        // {
        //     printf("%02x",event->disc.data[i]);
        // }
        // printf("\r\n\r\n");

        uint8_t len = event->disc.length_data;
        char *adv_str = (char *)malloc(len + 1);
        memcpy(adv_str, event->disc.data, len);

        adv_str[len] = '\0';

        // for (int i = 0; i < event->disc.length_data; i++)
        // {
        //     printf("%02x",adv_str[i]);
        // }
        // printf("\r\n\r\n");

        pika_eventListener_send(g_pika_ble_listener,_IRQ_SCAN_RESULT,
            arg_newObj(New_pikaTupleFrom(
                    arg_newInt(_IRQ_SCAN_RESULT),
                    arg_newInt(event->disc.addr.type),
                    arg_newBytes(addr,6),
                    arg_newInt(event->disc.event_type),
                    arg_newInt(event->disc.rssi),
                    arg_newStr(adv_str)
                    )));
        free(adv_str);
        return 0;

    case BLE_GAP_EVENT_DISC_COMPLETE: // 扫描结束
    // MicroPython None
        printf("discovery complete; reason=%d\r\n",event->disc_complete.reason);
        pika_eventListener_send(g_pika_ble_listener,_IRQ_SCAN_DONE,
            arg_newObj(New_pikaTupleFrom(
                    arg_newInt(_IRQ_SCAN_DONE),
                    arg_newInt(event->disc_complete.reason)
                    )));
        return 0;

    case BLE_GAP_EVENT_ADV_COMPLETE: //广播完成
    // MicroPython 没有这个事件
        printf("advertise complete; reason=%d\r\n",event->adv_complete.reason);
        return 0;

    case BLE_GAP_EVENT_ENC_CHANGE:
    // 暂时不理
        /* Encryption has been enabled or disabled for this connection. */
        printf("encryption change event; status=%d \r\n",event->enc_change.status);
        rc = ble_gap_conn_find(event->enc_change.conn_handle, &desc);
        assert(rc == 0);
        print_conn_desc(&desc);
        MODLOG_DFLT(INFO, "\n");
        return 0;

    case BLE_GAP_EVENT_PASSKEY_ACTION :
    // 暂时不理
        printf("PASSKEY_ACTION_EVENT started \r\n");
        struct ble_sm_io pkey = {0};
        int key = 0;

        if (event->passkey.params.action == BLE_SM_IOACT_DISP) {
            pkey.action = event->passkey.params.action;
            pkey.passkey = 123456; // This is the passkey to be entered on peer
            ESP_LOGI(tag, "Enter passkey %" PRIu32 "on the peer side", pkey.passkey);
            rc = ble_sm_inject_io(event->passkey.conn_handle, &pkey);
            ESP_LOGI(tag, "ble_sm_inject_io result: %d\n", rc);
        } else if (event->passkey.params.action == BLE_SM_IOACT_NUMCMP) {
            ESP_LOGI(tag, "Passkey on device's display: %" PRIu32 , event->passkey.params.numcmp);
            ESP_LOGI(tag, "Accept or reject the passkey through console in this format -> key Y or key N");
            pkey.action = event->passkey.params.action;
            // if (scli_receive_key(&key)) {
            //     pkey.numcmp_accept = key;
            // } else {
            //     pkey.numcmp_accept = 0;
            //     ESP_LOGE(tag, "Timeout! Rejecting the key");
            // }
            rc = ble_sm_inject_io(event->passkey.conn_handle, &pkey);
            ESP_LOGI(tag, "ble_sm_inject_io result: %d\n", rc);
        } else if (event->passkey.params.action == BLE_SM_IOACT_OOB) {
            static uint8_t tem_oob[16] = {0};
            pkey.action = event->passkey.params.action;
            for (int i = 0; i < 16; i++) {
                pkey.oob[i] = tem_oob[i];
            }
            rc = ble_sm_inject_io(event->passkey.conn_handle, &pkey);
            ESP_LOGI(tag, "ble_sm_inject_io result: %d\n", rc);
        } else if (event->passkey.params.action == BLE_SM_IOACT_INPUT) {
            ESP_LOGI(tag, "Enter the passkey through console in this format-> key 123456");
            pkey.action = event->passkey.params.action;
            // if (scli_receive_key(&key)) {
            //     pkey.passkey = key;
            // } else {
            //     pkey.passkey = 0;
            //     ESP_LOGE(tag, "Timeout! Passing 0 as the key");
            // }
            rc = ble_sm_inject_io(event->passkey.conn_handle, &pkey);
            ESP_LOGI(tag, "ble_sm_inject_io result: %d\n", rc);
        }
        return 0;

    case BLE_GAP_EVENT_NOTIFY_RX: // 客户端

        printf("received %s; conn_handle=%d attr_handle=%d attr_len=%d",
                event->notify_rx.indication ? "indication" : "notification",
                event->notify_rx.conn_handle,
                event->notify_rx.attr_handle,
                OS_MBUF_PKTLEN(event->notify_rx.om));
        printf("\r\n");
        if(event->notify_rx.indication == 1){ // indication
            // MicroPython : conn_handle, value_handle, notify_data
            uint16_t len = event->notify_rx.om->om_len;
            char *indic_str = (char *)malloc(len + 1);
            memcpy(indic_str, event->notify_rx.om->om_data, len);
            indic_str[len] = '\0';

            pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_INDICATE,
                arg_newObj(New_pikaTupleFrom(
                        arg_newInt(_IRQ_GATTC_INDICATE),
                        arg_newInt(event->notify_rx.conn_handle),
                        arg_newInt(event->notify_rx.attr_handle),
                        arg_newStr(indic_str)
                        )));
            free(indic_str);
        }
        else { 
            uint16_t len = event->notify_rx.om->om_len;
            char *indic_str = (char *)malloc(len + 1);
            memcpy(indic_str, event->notify_rx.om->om_data, len);
            indic_str[len] = '\0';

            pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_NOTIFY,
                arg_newObj(New_pikaTupleFrom(
                        arg_newInt(_IRQ_GATTC_NOTIFY),
                        arg_newInt(event->notify_rx.conn_handle),
                        arg_newInt(event->notify_rx.attr_handle),
                        arg_newStr(indic_str)
                        )));
            free(indic_str);
        }
        
        return 0;

    case BLE_GAP_EVENT_NOTIFY_TX: //通知发送完成
        printf("notify_tx event; conn_handle=%d attr_handle=%d status=%d is_indication=%d\r\n",
                    event->notify_tx.conn_handle,
                    event->notify_tx.attr_handle,
                    event->notify_tx.status,
                    event->notify_tx.indication);
        if(event->notify_tx.indication == 1){ // indication
            // MicroPython : conn_handle, value_handle, notify_data
            pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_INDICATE_DONE,
                arg_newObj(New_pikaTupleFrom(
                        arg_newInt(_IRQ_GATTS_INDICATE_DONE),
                        arg_newInt(event->notify_tx.conn_handle),
                        arg_newInt(event->notify_tx.attr_handle),
                        arg_newInt(event->notify_tx.status)
                        )));
        }        
        return 0;

    case BLE_GAP_EVENT_SUBSCRIBE://订阅 客户端向服务端订阅
        printf("subscribe event; conn_handle=%d attr_handle=%d "
                    "reason=%d prevn=%d curn=%d previ=%d curi=%d\r\n",
                    event->subscribe.conn_handle,
                    event->subscribe.attr_handle,
                    event->subscribe.reason,
                    event->subscribe.prev_notify,
                    event->subscribe.cur_notify,
                    event->subscribe.prev_indicate,
                    event->subscribe.cur_indicate);
        pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_SUBSCRIBE,
        arg_newObj(New_pikaTupleFrom(
                arg_newInt(_IRQ_GATTC_SUBSCRIBE),
                arg_newInt(event->subscribe.conn_handle),
                arg_newInt(event->subscribe.attr_handle),
                arg_newInt(event->subscribe.reason)
                )));
        return 0;

    case BLE_GAP_EVENT_MTU:
        MODLOG_DFLT(INFO, "mtu update event; conn_handle=%d cid=%d mtu=%d\n",
                    event->mtu.conn_handle,
                    event->mtu.channel_id,
                    event->mtu.value);
        return 0;

    case BLE_GAP_EVENT_IDENTITY_RESOLVED:
        return 0;

    case BLE_GAP_EVENT_REPEAT_PAIRING:
        /* We already have a bond with the peer, but it is attempting to
         * establish a new secure link.  This app sacrifices security for
         * convenience: just throw away the old bond and accept the new link.
         */

        /* Delete the old bond. */
        rc = ble_gap_conn_find(event->repeat_pairing.conn_handle, &desc);
        assert(rc == 0);
        ble_store_util_delete_peer(&desc.peer_id_addr);

        /* Return BLE_GAP_REPEAT_PAIRING_RETRY to indicate that the host should
         * continue with the pairing operation.
         */
        return BLE_GAP_REPEAT_PAIRING_RETRY;

        case BLE_GAP_EVENT_PHY_UPDATE_COMPLETE:
            return 0;

        case BLE_GAP_EVENT_EXT_DISC:
            return 0;

        case BLE_GAP_EVENT_PERIODIC_SYNC:
            return 0;

        case BLE_GAP_EVENT_PERIODIC_REPORT:
            return 0;

        case BLE_GAP_EVENT_PERIODIC_SYNC_LOST:
            return 0;

        case BLE_GAP_EVENT_SCAN_REQ_RCVD:
            return 0;

        case BLE_GAP_EVENT_PERIODIC_TRANSFER:
            return 0;

        case BLE_GAP_EVENT_PATHLOSS_THRESHOLD:
            return 0;

        case BLE_GAP_EVENT_TRANSMIT_POWER:
            return 0;

        case BLE_GAP_EVENT_SUBRATE_CHANGE:// 这个是啥事件？
            return 0;
    }
    return 0;
}

// GATT 查找所有服务回调函数
static int ble_gatt_disc_all_svcs_cb(uint16_t conn_handle,
                                 const struct ble_gatt_error *error,
                                 const struct ble_gatt_svc *service,
                                 void *arg){

// pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTS_INDICATE_DONE,
//     arg_newObj(New_pikaTupleFrom(
//             arg_newInt(_IRQ_GATTS_INDICATE_DONE),
//             arg_newInt(event->notify_tx.conn_handle),
//             arg_newInt(event->notify_tx.attr_handle),
//             arg_newStr(event->notify_tx.status)
//             )));
    return 0; 
}

// GATT 查找所有服务回调函数
static int ble_gatt_disc_svcs_by_uuid_cb(uint16_t conn_handle,
                                 const struct ble_gatt_error *error,
                                 const struct ble_gatt_svc *service,
                                 void *arg){
    return 0;
}

// GATT 查找所有特性回调函数
static int ble_gatt_disc_all_chrs_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            const struct ble_gatt_chr *chr, void *arg){
                                
    return 0;
}

// GATT 查找特定UUID特性回调函数
static int ble_gatt_disc_chrs_by_uuid_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            const struct ble_gatt_chr *chr, void *arg){
    return 0;
}


// GATT 查找所有描述符回调函数
static int ble_gatt_disc_all_dscs_cb(uint16_t conn_handle,
                            const struct ble_gatt_error *error,
                            uint16_t chr_val_handle,
                            const struct ble_gatt_dsc *dsc,
                            void *arg){
    pika_eventListener_send(g_pika_ble_listener,_IRQ_GATTC_DESCRIPTOR_RESULT,
        arg_newObj(New_pikaTupleFrom(
                arg_newInt(_IRQ_GATTC_DESCRIPTOR_RESULT),
                arg_newInt(conn_handle),
                arg_newInt(dsc->handle) //,
                // arg_newStr(dsc->uuid.value) //TODO:UUID传递方法
                )));
    
    return 0;
}