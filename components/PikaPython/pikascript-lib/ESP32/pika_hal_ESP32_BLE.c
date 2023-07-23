#include "pikaScript.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "host/util/util.h"
#include "services/gap/ble_svc_gap.h"
#include "esp_log.h"
#include "nvs_flash.h"

#define printf __platform_printf

void bluetooth_BLE_active(PikaObj *self)
{
    printf("active BLE\r\n");

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

void bluetooth_BLE_init(PikaObj *self)
{
    printf("init pikapython BLE");
}

void bluetooth_BLE_test(PikaObj *self)
{
    printf("test");
}

void bluetooth_BLE_gap_advertise(PikaObj *self)
{
    printf("gap_advertise");
}