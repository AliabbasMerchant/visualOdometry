#include <IO16.h>
#include <SRA16.h>
#include <Wire.h>
#include <MechaQMC5883.h>


#define COMM_DELAY 100

#define ACKNOWLEDGE "ack"
#define EXECUTED "ok"


MechaQMC5883 qmc;  //Magnetometer Object


String input;   //String to hold the Input data from the Raspberry-pi

////******************************Commands********************************************//
//Syntax : "(command)(value)"
//example : "w1000"
//Command List:
//"w","value" = forward , duration
//"s","value" = backward , duration
//"r","value" = rotate , absolute-Target Heading Angle



bool isReceiving = false;
int heading_angle;



void setup() {
//Initialise I2C Communication with The Magnetometer
  Wire.begin();
  qmc.init();
  qmc.setMode(Mode_Continuous,ODR_200Hz,RNG_2G,OSR_256);

 //Initialise Serial Communication 
  Serial.begin(9600);
  
  //Initialize all the PORTS and Movement Stuff
  port_init();
  bot_motion_init();
  set_pwm1a(400);
  set_pwm1b(400);


  DDRC = 0xFF;
  DDRA = 0xFF;

  UpdateCurrentAngle();
}

void loop() 
{
  processData();
  UpdateCurrentAngle();
}
  
void UpdateCurrentAngle()
{
  int x,y,z;
  qmc.read(&x,&y,&z,&heading_angle);
}


  

  void processData(void)      //Process if any Command/Instruction is Received
  {
    while (Serial.available())
    {
    isReceiving = true;
      delay(3);         //delay to allow the buffer to fill
      if(Serial.available() >0)
        {
        char in = Serial.read();  //gets one byte from the String
        input += in;
        
        } 
    }

  if(isReceiving)   //Process input if any command is Received.
      {
        Parse_input(input);
      }

    if(isReceiving)
    {
      isReceiving = false;
      }
      serialFlush();
      input="";
    delay(COMM_DELAY);
  }





//Execute Commands 
void Parse_input(String in)      
{
  char command  = in[0];    //first letter of the input is a command keyword
  int value = 0;            //magnitude or size of the command
  for(int i=1;i<in.length();i++)
  {
    value = 10*value + (int)in[i]-48;
  }

  //execute Functions

  switch(command)
  {
    case 'w':     //forward command
      forward(value);
      break;
    case 's':     //backward command
      backward(value);
      break;
    case 'r':     //rotate
      rotate(value);
      break;
    case 'g':
    	get_angle();
    	break;
  }

  }




//Bot Motion Functions

    void forward(int time_in_ms)
    {
      acknowledge();
      bot_forward();
      delay(time_in_ms);
      bot_brake();
      executed();
      
    }
    void backward(int time_in_ms)
    {
      acknowledge();
      bot_backward();
      delay(time_in_ms);
      bot_brake();
      executed();
    }
    void rotate(int target_angle)
    {
      acknowledge();
      
      if(target_angle > heading_angle)
      {
        while(abs(target_angle-heading_angle) >= 2 )
        {
          
          bot_spot_left();
          if(heading_angle >= target_angle)
          {
            break;
          }
          UpdateCurrentAngle();
        }
      }
      else
      {
        while(abs(heading_angle - target_angle) >=2 )
        {
      
          bot_spot_right();
          if(heading_angle<target_angle)
          {
            break;
          }
          UpdateCurrentAngle();
        }
      }
    bot_brake();

    executed();
    }

    void get_angle()
    {
    	acknowledge();
    	UpdateCurrentAngle();
    	Serial.println(heading_angle);
    }



//Flush the Serial Buffer
  void serialFlush()
  {
    byte w = 0;

    for(int i=0;i<10;i++)
    {
      while(Serial.available()>0)
      {
        char t = Serial.read();
        w++;
        delay(1);
        }
        delay(1);
      
      }
  }


//Flag Messages to the Raspberrypi on Receiving and Executing Instructions
  void acknowledge()
  {
    Serial.println(ACKNOWLEDGE);
  }

  void executed()
  {
    Serial.println(EXECUTED);
  }
