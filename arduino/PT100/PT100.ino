
// Declaracion de variables globales
float raw; // Variable para almacenar el valor obtenido del sensor (0 a 1023)
float vT;
float rT;
int pinLM35 = 0; // Variable del pin de entrada del sensor (A0)

 
void setup() {
  // Configuramos el puerto serial a 9600 bps
  Serial.begin(9600);
 
}
 
void loop() {
  // Con analogRead leemos el sensor, recuerda que es un valor de 0 a 1023
  raw = analogRead(A0); 
  Serial.print(raw);
  Serial.print(",");
  
  // vT eq
  vT = (5.0 * raw)/1023.0;
  Serial.print(vT);
  Serial.print(",");
 
  rT = (100.0*vT)/(5.0-vT);
  Serial.println(rT);

  // Esperamos un tiempo para repetir el loop
  delay(1000);
}
