#define FLEX1 A0
#define FLEX2 A1

class CapteurFlex{
  public:
    CapteurFlex(int value);  // Constructeur
    void setup(void); // Initialisation du capteur
    void calibrage(void); //Fonction de calibrage
    int vlrAngle(void); //Fonction qui retourne un angle à partir d'une tension
    void lectureTension(void); //Lecture de la tension 
  private:
    int pin;
    int tension;
    int pos;
    int calib0;
    int calib180;
};

//Constructuer du capteur de flexion
CapteurFlex::CapteurFlex(int value){ 
  pin = value;
  tension = 0;
  pos = 0;
  calib0 = 0;
  calib180 = 0;
}

//Initialisation du capteur de flexion
void CapteurFlex::setup(void){ pinMode(pin, INPUT);}

//Fonction de calibrage du capteur de flexion
void CapteurFlex::calibrage(void){
  calib180 = analogRead(pin); 
  delay(2000);
  calib0 = analogRead(pin); 
  delay(2000);
}

//Lit la valeur de la tension
void CapteurFlex::lectureTension(void){
  tension = analogRead(pin);
  pos = vlrAngle();
  delay(500);
}

//Permet de calculer l'angle en fonction de la tension reçue
int CapteurFlex::vlrAngle(void){ 
  if(tension < calib180) return 180; //Si la tension est supérieure à celle obtenue lors du calibrage
  else if(tension > calib0) return 0; //Si la tension est inférieure à celle obtenue lors du calibrage
  else return map(tension, calib0, calib180, 0, 180); //Calcul de l'angle en fonction des paramètres initiaux                                       
}

//Déclarations
CapteurFlex flex1(FLEX1);
CapteurFlex flex2(FLEX2);

void setup() {
  Serial.begin(9600);
  flex1.setup();
  flex2.setup();
  flex1.calibrage();
  flex2.calibrage();
}

void loop() {
  flex1.lectureTension();
  flex2.lectureTension();
}
