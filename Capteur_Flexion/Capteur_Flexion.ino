class CapteurFlex{ //extension d'une classe mère capteur
    private:
    int pin;
    int tension;
    int pos;
    int calib0;
    int calib180;
  public:
    Capteur(int value);  // Constructeur
    void setup(); // Initialisation du capteur
    void calibrage(); //Fonction de calibrage
    int vlrAngle(); //Fonction qui retourne un angle à partir d'une tension
    void lectureTension(); //Lecture de la tension 
}

//Constructuer du capteur de flexion
CapteurFlex::CapteurFlex(int value){ 
  pin = value;
  tension = 0;
  pos = 0;
  calib0 = 0;
  calib180 = 0;
}

//Initialisation du capteur de flexion
void CapteurFlex::setup(){ pinMode(pin, INPUT);}

//Fonction de calibrage du capteur de flexion
void CapteurFlex::calibrage(){
  calib180 = analogRead(pin); 
  delay(2000);
  calib0 = analogRead(pin); 
  delay(2000);
}

//Lit la valeur de la tension
void CapteurFlex::lectureTension(){
  tension = analogRead(pin);
  pos = vlrAngle(tension, calib180, calib0);
  delay(500);
}

//Permet de calculer l'angle en fonction de la tension reçue
int CapteurFlex::vlrAngle(){ 
  if(tension < calib180) return 180; //Si la tension est supérieure à celle obtenue lors du calibrage
  else if(tension > calib0) return 0; //Si la tension est inférieure à celle obtenue lors du calibrage
  else return map(tension, calib0, calib180, 0, 180); //Calcul de l'angle en fonction des paramètres initiaux                                       
}

//Déclarations
Capteur flex1(A0);
Capteur flex2(A1);

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
