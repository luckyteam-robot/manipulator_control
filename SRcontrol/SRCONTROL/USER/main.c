#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "pwm.h"

int main(void)
{ 
 
	u8 len,t;	    //接受数据的个数
	u16 times=0;  
	u16 val[2];   //tim3的两路通道的计数值
	u16 servo0pwmval=0; //第一路pwm信号占空比（舵机0，即关节0的转动信息）
  u16 servo1pwmval=0; //第二路pwm信号占空比（舵机1，即关节1的转动信息）
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//设置系统中断优先级分组2（2中断抢占，2.。。。）
	delay_init(168);		//延时初始化 
	TIM3_PWM_Init(200-1,8400-1);	//84M/8400=0.01Mhz的计数频率,重装载值500，所以PWM频率为 0.01M/200=50hz. 舵机周期大约为20ms
	uart_init(115200);	//串口初始化波特率为115200
	LED_Init();		  		//初始化与LED连接的硬件接口  
	while(1)
	{   //USART_RX_STA：接受状态寄存器
		if(USART_RX_STA&0x8000)  //是否接收数据完成（1000，0000， 0000， 0000）
		{					   
			len=USART_RX_STA&0x3fff;//得到此次接收到的数据长度（0011， 1111， 1111， 1111）
			if(len==2)   //只有电脑发送的是2个数据时，才执行操作
			{
				servo0pwmval = USART_RX_BUF[0];
				servo1pwmval = USART_RX_BUF[1];
				USART_SendData(USART1, servo0pwmval);//发送需要用16进制数发送；175-195（即AFH- C3H）
				TIM_SetCompare1(TIM3,servo0pwmval);	//修改比较值，修改占空比
				TIM_SetCompare2(TIM3,servo1pwmval);	//修改比较值，修改占空比
				printf("\r\n处理数据中\r\n");
			}
			else if(len==1){//请求发送当前舵机的角度,即查询TIM的计数器值
				printf("\r\n当前关节角：\r\n");
				val[0] = TIM3->CCR1;
				val[1] = TIM3->CCR2;
				for(t=0;t<2;t++){
						USART_SendData(USART1, val[t]);         //向串口1发送数据
						while(USART_GetFlagStatus(USART1,USART_FLAG_TC)!=SET);//等待发送结束
				}
			}
			else {
					printf("\r\n输入参数错误（即只能输入2个关节角数据），请重新输入!\r\n");
			}
			USART_RX_STA=0;   //处理完数据，清除数据接受完标志，为下次接受数据做准备。
		}
		else{						//数据尚未接受完或者无数据接受时
			times++;
			if(times%500==0)printf("请输入关节角数据,以回车键结束\r\n");  
			if(times%30==0)LED0=!LED0;//闪烁LED,提示系统正在运行.
			delay_ms(10);   
		}
	}
}

