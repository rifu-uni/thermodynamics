float vref = 5.0;
int pinLM35 = A0;
int pinDiod = A2;
unsigned long t0;
float t;

// intervalo de muestreo en milisegundos (0.25 s = 250 ms)
const unsigned long intervalo = 250;

void setup() {
  Serial.begin(9600);
  t0 = millis();
  Serial.println("t,rawLM35,voltLM35,rawDiodo,voltDiodo");
}

void loop() {
  static unsigned long previo = 0;
  unsigned long ahora = millis();
  
  if (ahora - previo >= intervalo) {
    previo = ahora;
    t = (ahora - t0) / 1000.0;  // tiempo en segundos
    
    int rawL = analogRead(pinLM35);
    int rawD = analogRead(pinDiod);
    float vL = (vref * rawL) / 1023.0;
    float vD = (vref * rawD) / 1023.0;

    Serial.print(t, 3); Serial.print(",");
    Serial.print(rawL); Serial.print(",");
    Serial.print(vL, 4); Serial.print(",");
    Serial.print(rawD); Serial.print(",");
    Serial.println(vD, 4);
  }
}