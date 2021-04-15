#include <Wire.h>
//#include <Adafruit_TMP117.h>
//#include <Adafruit_Sensor.h>
//Adafruit_TMP117  tmp117;

//---------------------CLASSES CAPTEURS----------------------------
class CapteurFlex{
  private:
    int tension;
    int pos;
    int calib90;
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
    String nom;  
  public:
    Doigt(CapteurFlex f1, CapteurPressure p1, CapteurPressure p2, CapteurTemp t1, CapteurTemp t2, String mot);
    void setUp();  
    void lecture();
};

//---------------------CLASS DOIGTS--------------------------------
class Main{
  private:
    const int nb = 2;
    Doigt doigts[];
  public:
    Main(Doigt d1, Doigt d2);
    void setUp();  
    void lecture();
};

//---------------------------CONSTRUCTEURS-----------------------------

//Constructeur du capteur de flexion
CapteurFlex::CapteurFlex(int value){ 
  pin = value;
  tension = 0;
  pos = 0;
  calib90 = 0;
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

//Constructeur de de la classe doigt
Doigt::Doigt(CapteurFlex f1, CapteurPressure p1, CapteurPressure p2, CapteurTemp t1, CapteurTemp t2, String mot){
  flex = f1;
  pressure1 = p1;
  pressure2 = p2;
  temp1 = t1;
  temp2 = t2;
  nom = mot;
}

//Constructeur de la classe Main
Main::Main(Doigt d1, Doigt d2){
  doigts[0] = d1;
  doigts[1] = d2;
}

//----------------------FONCTIONS SETUP----------------------------------

//Initialisation du capteur de flexion
void CapteurFlex::setUp(){ pinMode(pin, INPUT);}

//Initialisation du capteur de pression
void CapteurPressure::setUp(){ pinMode(pinPressure, INPUT);}

//Initialisation du capteur de temperature
void CapteurTemp::setUp(){ pinMode(pinSensor, INPUT);}

//Initialisation d'un doigt
void Doigt::setUp() {
  flex.setUp();
  pressure1.setUp();
  pressure2.setUp();
  temp1.setUp();
  temp2.setUp();
  Serial.print("Commencement du calibrage pour le ");
  Serial.println(nom);
  flex.calibrage();
}

//Initialisation de la main
void Main::setUp() {
  for(int i=0; i < nb; i++) doigts[i].setUp();
}

//---------------------FONCTION CALIBRATION CAPTEURS FLEXION------------

//Fonction de calibrage du capteur de flexion
void CapteurFlex::calibrage(){
  Serial.print("Calibrage pour 180 : ");
  delay(2000);
  calib180 = analogRead(pin);
  Serial.println(calib180);
  delay(1000);
  Serial.print("Calibrage pour 90 : ");
  delay(2000);
  calib90 = analogRead(pin); 
  Serial.println(calib90); 
  delay(1000);
}


//---------------------FONCTION CALCUL ANGLE CAPTEURS FLEXION-----------

//Permet de calculer l'angle en fonction de la tension reçue
int CapteurFlex::vlrAngle(){ 
  if(tension < calib180) return 180; //Si la tension est supérieure à celle obtenue lors du calibrage
  else if(tension > calib90) return 90; //Si la tension est inférieure à celle obtenue lors du calibrage
  else return map(tension, calib90, calib180, 90, 180); //Calcul de l'angle en fonction des paramètres initiaux                                       
}

//----------------------FONCTIONS LIT LES VALEURS-----------------------

//Lit la valeur de la tension
void CapteurFlex::lectureTension(){
  tension = analogRead(pin);
  pos = vlrAngle();
  Serial.print(pos);
}

//Lit la valeur en bit du capteur de pression
void CapteurPressure::lecturePressure(){
  reading = analogRead(pinPressure);  
  Serial.print(reading);
}

//Lit la valeur en degre du capteur de temperature
void CapteurTemp::lectureTemp(){
  /*sensors_event_t temp; // create an empty event to be filled
  tmp117.getEvent(&temp);
  Serial.print(temp.temperature);
  Serial.print(" \xC2\xB0"); // shows degree symbol
  Serial.print("C");*/
}


void Doigt::lecture(){
  Serial.print("\n\t\t\t\t");
  Serial.println(nom);
  Serial.println("CapteurFlex\t\tCapteurPressure\t\tCapteurTemp");
  Serial.print("\t");
  flex.lectureTension();
  Serial.print("\t\t");
  pressure1.lecturePressure();
  Serial.print("\t|\t");
  pressure2.lecturePressure();
  /*Serial.print("\t\t");
  temp1.lectureTemp();
  Serial.print("\t|\t");
  temp2.lectureTemp();*/
  Serial.println();
  delay(500);
}

void Main::lecture(){
  for(int i=0; i < nb; i++) doigts[i].lecture();
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

Doigt pouce(flex1, pressure1, pressure2, temp1, temp2, "POUCE");
Doigt index(flex2, pressure3, pressure4, temp3, temp4, "INDEX");
Main lionne(pouce, index);

void setup() {
  Serial.begin(115200);
  lionne.setUp();
}

void loop() {
  lionne.lecture();
}
