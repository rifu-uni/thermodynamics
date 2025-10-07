
// Declaracion de variables globales
int pinPT1 = 1;
float rawPT1; // Variable para almacenar el valor obtenido del sensor (0 a 1023)
float vPT1;
float rPT1;

int pinTER = 5;
float rawTER;
float vTER;
float rTER;

 
void setup() {
  // Configuramos el puerto serial a 9600 bps
  Serial.begin(9600);
}
 

void loop() {
  // PT100 sensor reading
  rawPT1 = analogRead(A1); 
  Serial.print(rawPT1);
  Serial.print(",");
  
  // vT eq
  vPT1 = vT(rawPT1);
  Serial.print(vPT1);
  Serial.print(",");
 
  rPT1 = rT(vPT1);
  Serial.print(rPT1);
  Serial.print(",");


  // Termistor sensor reading
  rawTER = analogRead(A5);
  Serial.print(rawTER);
  Serial.print(",");

  vTER = vT(rawTER);
  Serial.print(vTER);
  Serial.print(",");

  rTER = rT(vTER);
  Serial.println(rTER);
  

  // Esperamos un tiempo para repetir el loop
  delay(1000);
}

float vT(float i) {
  return (5.0 * i)/1023.0;
}

float rT(float i) {
  return (100.0*i)/(5.0-i);
}