/*
 * [Warning!] This file is auto-generated by pika compiler.
 * Do not edit it manually.
 * The source code is *.pyi file.
 * More details: 
 * English Doc:
 * https://pikadoc-en.readthedocs.io/en/latest/PikaScript%20%E6%A8%A1%E5%9D%97%E6%A6%82%E8%BF%B0.html
 * Chinese Doc:
 * http://pikapython.com/doc/PikaScript%20%E6%A8%A1%E5%9D%97%E6%A6%82%E8%BF%B0.html
 */

#ifndef __PikaStdDevice_UART__H
#define __PikaStdDevice_UART__H
#include <stdio.h>
#include <stdlib.h>
#include "PikaObj.h"

PikaObj *New_PikaStdDevice_UART(Args *args);

void PikaStdDevice_UART___init__(PikaObj *self);
void PikaStdDevice_UART_close(PikaObj *self);
void PikaStdDevice_UART_disable(PikaObj *self);
void PikaStdDevice_UART_enable(PikaObj *self);
void PikaStdDevice_UART_platformDisable(PikaObj *self);
void PikaStdDevice_UART_platformEnable(PikaObj *self);
void PikaStdDevice_UART_platformRead(PikaObj *self);
void PikaStdDevice_UART_platformReadBytes(PikaObj *self);
void PikaStdDevice_UART_platformWrite(PikaObj *self);
void PikaStdDevice_UART_platformWriteBytes(PikaObj *self);
char* PikaStdDevice_UART_read(PikaObj *self, int length);
Arg* PikaStdDevice_UART_readBytes(PikaObj *self, int length);
void PikaStdDevice_UART_setBaudRate(PikaObj *self, int baudRate);
void PikaStdDevice_UART_setCallBack(PikaObj *self, Arg* eventCallBack, int filter);
void PikaStdDevice_UART_setCallback(PikaObj *self, Arg* eventCallBack, int filter);
void PikaStdDevice_UART_setDataBits(PikaObj *self, int dataBits);
void PikaStdDevice_UART_setFlowControl(PikaObj *self, int flowControl);
void PikaStdDevice_UART_setId(PikaObj *self, int id);
void PikaStdDevice_UART_setParity(PikaObj *self, int parity);
void PikaStdDevice_UART_setPinCTS(PikaObj *self, char* pin);
void PikaStdDevice_UART_setPinRTS(PikaObj *self, char* pin);
void PikaStdDevice_UART_setPinRX(PikaObj *self, char* pin);
void PikaStdDevice_UART_setPinTX(PikaObj *self, char* pin);
void PikaStdDevice_UART_setStopBits(PikaObj *self, int stopBits);
void PikaStdDevice_UART_write(PikaObj *self, char* data);
void PikaStdDevice_UART_writeBytes(PikaObj *self, uint8_t* data, int length);

#endif
