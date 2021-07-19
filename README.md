# HW3_P2

En la parte a) se programa el funcionamiento de cargas consistentes (que en la parte 1 de la tarea se habían ingresado las cargas manualmente), se revisó el funcionamiento para cualquier malla y esta se encuentra en el archivo "nodal_loads.py".

Para la parte b) se utilizó la malla que se solicitaba en la Tarea 3 - Parte 1 con un total de 18264 nodos (archivo "placa_plana_a.msh"), una malla intermedia con 2546 nodos ("placa_plana_b.msh") y la malla vista en clases con 292 nodos ("placa_plana_c.msh"). A continuación se muestran los resultados obtenidos para cada malla:

MALLA a): Detallada.
![imagen](https://user-images.githubusercontent.com/81662690/126212375-74610cd4-1de5-4e2c-ab0f-2d55cc332e83.png)

Sigma x:
![imagen](https://user-images.githubusercontent.com/81662690/126212633-c0970703-5820-4ece-bcf5-c60d467f2348.png)
![imagen](https://user-images.githubusercontent.com/81662690/126212745-837b7890-b20c-40cf-aa8c-0e27b30ab0cb.png)

Desplazamiento (aplificado en 1e8):
![imagen](https://user-images.githubusercontent.com/81662690/126213064-6c13dc2f-4f42-42d6-92d9-7bc711c3e308.png)


MALLA b): Intermedia.
![imagen](https://user-images.githubusercontent.com/81662690/126213993-1b5447f5-5a70-4d62-b109-312f7aa710cd.png)

Sigma x:
![imagen](https://user-images.githubusercontent.com/81662690/126214152-61ba420c-162a-414c-8659-dc3a576e1ab6.png)

Desplazamiento (amplificado en 1e8):
![imagen](https://user-images.githubusercontent.com/81662690/126214416-9de6279d-135d-4bc6-b009-e9de1c8231f4.png)


MALLA c): Usada en clases.
![imagen](https://user-images.githubusercontent.com/81662690/126214742-596b6561-93fc-47bf-88ab-676ce26729ff.png)

Sigma x:
![imagen](https://user-images.githubusercontent.com/81662690/126214668-239cd6ae-c456-48c7-a584-e687f7c2bfc9.png)

Desplazamiento (amplificado en 1e7):
![imagen](https://user-images.githubusercontent.com/81662690/126214884-5bd5063e-1815-4dd3-a42d-ba70457c5bc1.png)

Al haber menor detalle de la malla, es desplazamiento y la tensión disminuye ya que se "junta" una sección más grande en donde la tensión en la misma por lo que el máximo va a tender a disminuir al promediarse con valores más bajos. El problema que tiene el refinar mucho la malla es el recurso computacional utilizado ya que la malla más detallada se demoró aproximadamente 48 horas en correr usando matrices dispersas, a diferencia de la vista en clases que se demora menos de 1 minuto, mientras que la intermedia se demoró entre 1 y 2 horas.

Para elegir la malla que es más adecuada, se debe revisar el nivel de análisis y resultados que se desea alcanzar ya que no me va a servir una malla tan refinada si me entrega resultados mucho más detallados de los que necesito, se debe optimizar el recurso computacional y tampoco usar una malla poco refinada que no me va a dar resultados correctos.
