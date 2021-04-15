#include <Wire.h>
#include <Adafruit_TMP117.h>
#include <Adafruit_Sensor.h>

Adafruit_TMP117  tmp117;



//---------------------CLASSES CAPTEURS----------------------------

class CapteurFlex{
  private:
    int tension;
    int pos;
    int calib0;
    int calib180;
    int pin;
    int regAddr; //adresse du registre dans laquelle est stockee la valeur
  public:
    CapteurFlex(): pin(-1){};
    CapteurFlex(int value);  // Constructeur
    void setUp(); // Initialisation du capteur
    void calibrage(); //Fonction de calibrage
    int vlrAngle(); //Fonction qui retourne un angle à partir d'une tension
    void lectureTension(); //Lecture de la tension 
};

class CapteurPressure{
  private:
    int pin1; //3 pin de selection du multiplexeur
    int pin2;
    int pin3;
    int pinPressure;
    int regAddr; //adresse du registre dans laquelle est stockee la valeur
    int reading;
  public:
    CapteurPressure(): pinPressure(-1){};
    CapteurPressure(int value); //Constructeur
    void setUp(); // Initialisation du capteur
    void lecturePressure(); //Lecture des valeurs des capteurs de force en bit
};

class CapteurTemp{
  private:
    int pinSensor;
    int readingSensor;
  public:
    CapteurTemp(): pinSensor(-1){};
    CapteurTemp(int value);
    void setUp();
    void lectureTemp();
};

//---------------------CLASS DOIGTS--------------------------------

class Doigt{
  private:
    CapteurFlex flex;
    CapteurPressure pressure1;
    CapteurPressure pressure2;
    CapteurTemp temp1;
    CapteurTemp temp2;   
  public:
    Doigt(CapteurFlex f1, CapteurPressure p1, CapteurPressure p2, CapteurTemp t1, CapteurTemp t2);
    void setUp();  
    void lectureTension();
};
//---------------------------CONSTRUCTEURS-----------------------------

//Constructeur du capteur de flexion
CapteurFlex::CapteurFlex(int value){ 
  pin = value;
  tension = 0;
  pos = 0;
  calib0 = 0;
  calib180 = 0;
}

//Constructeur du capteur de pression
CapteurPressure::CapteurPressure(int value){ 
  pinPressure = value;
  reading = 0;
}

//Constructeur du capteur de temperature
CapteurTemp::CapteurTemp(int value){ 
  pinSensor = value;
  readingSensor = 0;
}

Doigt::Doigt(CapteurFlex f1, CapteurPressure p1, CapteurPressure p2, CapteurTemp t1, CapteurTemp t2){
  flex = f1;
  pressure1 = p1;
  pressure2 = p2;
  temp1 = t1;
  temp2 = t2;
}


//----------------------FONCTIONS SETUP----------------------------------

//Initialisation du capteur de flexion
void CapteurFlex::setUp(){ pinMode(pin, INPUT);}

//Initialisation du capteur de pression
void CapteurPressure::setUp(){ pinMode(pinPressure, INPUT);}

//Initialisation du capteur de temperature
void CapteurTemp::setUp(){ pinMode(pinSensor, INPUT);}


void Doigt::setUp() {
  flex.setUp();
  pressure1.setUp();
  pressure2.setUp();
  temp1.setUp();
  temp2.setUp();
}

//---------------------FONCTION CALIBRATION CAPTEURS FLEXION------------

//Fonction de calibrage du capteur de flexion
void CapteurFlex::calibrage(){
  Serial.print("Calibrage 180 : ");
  delay(1000);
  calib180 = analogRead(pin); 
  delay(2000);
  Serial.println(calib180);
  Serial.print("Calibrage 0 : ");
  delay(1000);
  calib0 = analogRead(pin); 
  delay(2000);
  Serial.println(calib0);
}


//---------------------FONCTION CALCUL ANGLE CAPTEURS FLEXION-----------

//Permet de calculer l'angle en fonction de la tension reçue
int CapteurFlex::vlrAngle(){ 
  if(tension < calib180) return 180; //Si la tension est supérieure à celle obtenue lors du calibrage
  else if(tension > calib0) return 0; //Si la tension est inférieure à celle obtenue lors du calibrage
  else return map(tension, calib0, calib180, 0, 180); //Calcul de l'angle en fonction des paramètres initiaux                                       
}

//----------------------FONCTIONS LIT LES VALEURS-----------------------

//Lit la valeur de la tension
void CapteurFlex::lectureTension(){
  tension = analogRead(pin);
  pos = vlrAngle();
  Serial.print(tension);
}

//Lit la valeur en bit du capteur de pression
void CapteurPressure::lecturePressure(){
  reading = analogRead(pinPressure);  
  Serial.print(reading);
}

//Lit la valeur en degre du capteur de temperature
void CapteurTemp::lectureTemp(){
  sensors_event_t temp; // create an empty event to be filled
  tmp117.getEvent(&temp);
  Serial.print(temp.temperature);
  Serial.print(" \xC2\xB0"); // shows degree symbol
  Serial.print("C");
}


void Doigt::lectureTension(){
  Serial.println("\t\tCapteurFlex\t\t\t\tCapteurPressure\t\t\t\t\t\t\t\t\tCapteurTemp");
  Serial.print("|\t");
  flex.lectureTension();
  Serial.print("\t|\t");
  pressure1.lecturePressure();
  Serial.print("\t|\t");
  pressure2.lecturePressure();
  Serial.print("\t|\t");
  /*temp1.lectureTemp();
  Serial.print("\t|\t");
  temp2.lectureTemp();
  Serial.println("\t|\t");*/
  delay(500);
}

//----------------------DECLARATIONS DES CAPTEURS----------------------
//Déclarations capteurs flex
CapteurFlex flex1(A0);
CapteurFlex flex2(A1);

//Déclarations capteurs pressions
CapteurPressure pressure1(A2);
CapteurPressure pressure2(A3);
CapteurPressure pressure3(A4);
CapteurPressure pressure4(A5);

//Déclarations capteurs Temperatures
CapteurTemp temp1(A6);
CapteurTemp temp2(A7);
CapteurTemp temp3(A8);
CapteurTemp temp4(A9);

Doigt pouce(flex1, pressure1, pressure2, temp1, temp2);
Doigt index(flex2, pressure3, pressure4, temp3, temp4);

void setup() {
  Serial.begin(115200);
  pouce.setUp();
  index.setUp();
}

void loop() {
  pouce.lectureTension();
  index.lectureTension();
}
