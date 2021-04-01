#define FLEX1 A0
#define FLEX2 A1

#define PRESSURE1 A2
#define PRESSURE2 A3
#define PRESSURE3 A4
#define PRESSURE4 A5

#define TEMP1 A6
#define TEMP2 A7
#define TEMP3 A8
#define TEMP4 A9

class CapteurFlex{
  private:
    int pin;
    int tension;
    int pos;
    int calib0;
    int calib180;
  public:
    CapteurFlex(int value);  // Constructeur
    void setup(); // Initialisation du capteur
    void calibrage(); //Fonction de calibrage
    int vlrAngle(); //Fonction qui retourne un angle à partir d'une tension
    void lectureTension(); //Lecture de la tension 
};

class CapteurPressure{
  private:
    int pinPressure;
    int reading;
  public:
    CapteurPressure(int value); //Constructeur
    void setup(); // Initialisation du capteur
    void lectureBits(); //Lecture des valeurs des capteurs de force en bit
};

class CapteurTemp{
  private:
    int pinSensor;
    int readingSensor;
    float voltage;
    float temperature;
  public:
    CapteurTemp(int value);
    void setup();
    void lectureTemp();
};

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
  voltage = 0;
  temperature = 0;
}

//Initialisation du capteur de flexion
void CapteurFlex::setup(){ pinMode(pin, INPUT);}

//Fonction de calibrage du capteur de flexion
void CapteurFlex::calibrage(){
  
  calib180 = analogRead(pin);
  Serial.println(calib180); 
  delay(2000);
  calib0 = analogRead(pin); 
  Serial.println(calib0);
  delay(2000);
}

//Lit la valeur de la tension
void CapteurFlex::lectureTension(){
  tension = analogRead(pin);
  pos = vlrAngle();
  Serial.print(pos);
}

//Lit la valeur en bit du capteur de pression
void CapteurPressure::lectureBits(){
  reading = analogRead(pinPressure);  
  Serial.print(reading);
}

//Lit la valeur en degre du capteur de temperature
void CapteurTemp::lectureTemp(){
  readingSensor = analogRead(pinSensor);
  voltage = readingSensor * (5000 / 1024.0);
  temperature = (voltage - 500) / 10;
  Serial.print(temperature);
  Serial.print(" \xC2\xB0"); // shows degree symbol
  Serial.print("C");
}

//Permet de calculer l'angle en fonction de la tension reçue
int CapteurFlex::vlrAngle(){ 
  if(tension < calib180) return 180; //Si la tension est supérieure à celle obtenue lors du calibrage
  else if(tension > calib0) return 0; //Si la tension est inférieure à celle obtenue lors du calibrage
  else return map(tension, calib0, calib180, 0, 180); //Calcul de l'angle en fonction des paramètres initiaux                                       
}

//Déclarations capteurs flex
CapteurFlex flex1(FLEX1);
CapteurFlex flex2(FLEX2);

//Déclarations capteurs pressions
CapteurPressure pressure1(PRESSURE1);
CapteurPressure pressure2(PRESSURE2);
CapteurPressure pressure3(PRESSURE3);
CapteurPressure pressure4(PRESSURE4);

//Déclarations capteurs Temperatures
CapteurTemp temp1(TEMP1);
CapteurTemp temp2(TEMP2);
CapteurTemp temp3(TEMP3);
CapteurTemp temp4(TEMP4);

void setup() {
  Serial.begin(115200);
  flex1.setup();
  flex2.setup();
  flex1.calibrage();
  flex2.calibrage();
}

void loop() {
  Serial.println("\tCapteurFlex\t\t\t\t\tCapteurPressure\t\t\t\t\t\t\t\t\tCapteurTemp");
  Serial.print("|\t");
  flex1.lectureTension();
  Serial.print("\t|\t");
  flex2.lectureTension();
  Serial.print("\t||\t");
  
  pressure1.lectureBits();
  Serial.print("\t|\t");
  pressure2.lectureBits();
  Serial.print("\t|\t");
  pressure3.lectureBits();
  Serial.print("\t|\t");
  pressure4.lectureBits();
  Serial.print("\t||\t");
  
  temp1.lectureTemp();
  Serial.print("\t|\t");
  temp2.lectureTemp();
  Serial.print("\t|\t");
  temp3.lectureTemp();
  Serial.print("\t|\t");
  temp4.lectureTemp();
  Serial.println("\t|");
  
  delay(200);
}
