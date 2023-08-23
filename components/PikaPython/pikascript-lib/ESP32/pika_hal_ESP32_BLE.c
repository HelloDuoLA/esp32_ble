#include "pikaScript.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
// #include "nimble/host/include/host/ble_gap.h"
#include "host/ble_hs.h"
#include "host/util/util.h"
#include "services/gap/ble_svc_gap.h"
#include "esp_log.h"
#include "nvs_flash.h"

#define printf __platform_printf

void _bluetooth_BLE___init__(PikaObj *self)
{
    printf("Init BLE");
}

void _bluetooth_BLE_active(PikaObj *self)
{
    printf("Active BLE\r\n");
    /* Initialize NVS — it is used to store PHY calibration data */
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ret = nimble_port_init();
    if (ret != ESP_OK) {
        printf("Failed to init nimble %d \n", ret);
        return;
    }
    // ble_hs_cfg.sync_cb = blehr_on_sync;//在启动和重置后 host and controller 同步时 回调
    // ble_hs_cfg.reset_cb = blehr_on_reset;// host 致命错误 reset 时回调
}

void _bluetooth_BLE_test(PikaObj *self)
{
    printf("test");
}

void _bluetooth_BLE_gap_advertise(PikaObj *self)
{
    printf("gap_advertise");
}

int _bluetooth_BLE_gap_connect(PikaObj *self, int addr_type, char* addr, int64_t scan_duration_ms)
{
    printf("_bluetooth_BLE_gap_connect\r\n");
    return ble_gap_connect((uint8_t)addr_type,(ble_addr_t *)addr,scan_duration_ms,NULL,NULL,NULL);
}

int _bluetooth_BLE_gap_disconnect(PikaObj *self)
{
    printf("_bluetooth_BLE_gap_disconnect\r\n");
    return ble_gap_conn_cancel();
}

int _bluetooth_BLE_gap_scan(PikaObj *self, int duration_ms, int interval_us, int window_us, PIKA_BOOL active)
{
    printf("_bluetooth_BLE_gap_scan\r\n");
    struct ble_gap_disc_params *disc_params;
    disc_params = (struct ble_gap_disc_params*)malloc(sizeof(struct ble_gap_disc_params));
    disc_params->itvl = duration_ms / 0.625;
    disc_params->window = interval_us / 625;
    disc_params->filter_policy = BLE_HCI_SCAN_FILT_NO_WL;
    disc_params->passive = ~active;
    return ble_gap_disc(BLE_ADDR_PUBLIC, duration_ms, disc_params, NULL, NULL);
    // TODO:BLE_ADDR_TYPE_PUBLIC 与 BLE_ADDR_PUBLIC有无区别
}

int _bluetooth_BLE_gap_stop_scan(PikaObj *self)
{
    printf("_bluetooth_BLE_gap_stop_scan\r\n");
    return ble_gap_disc_cancel();
}

int _bluetooth_BLE_stop_advertise(PikaObj *self)
{
    printf("stop_advertise");
    return ble_gap_adv_stop();
}

// TODO:服务的内容该如何传递
int _bluetooth_BLE_register_a_service(PikaObj *self, PikaObj* service_info)
{
    printf("_bluetooth_BLE_register_a_service");
    return 0;
}

int _bluetooth_BLE_set_adv_data(PikaObj *self, char* data, int data_len)
{
    printf("_bluetooth_BLE_set_adv_data\r\n");
    return ble_gap_adv_set_data((uint8_t*)data,data_len);
}

int _bluetooth_BLE_set_rsp_data(PikaObj *self, char* data, int data_len)
{
    printf("_bluetooth_BLE_set_rsp_data\r\n");
    return ble_gap_adv_rsp_set_data((uint8_t*)data,data_len);
}

int _bluetooth_BLE_config_name_update(PikaObj *self, char* gap_name)
{
    struct ble_hs_adv_fields *adv_fields;
    adv_fields = (struct ble_hs_adv_fields*)malloc(sizeof(struct ble_hs_adv_fields));
    adv_fields->name = (unsigned char *)gap_name;
    // adv_fields->name_is_complete
    return ble_gap_adv_set_fields(adv_fields);
}