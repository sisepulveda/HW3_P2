# HW3_P2

![imagen](https://user-images.githubusercontent.com/81662690/127946329-c7baf5a2-a6b4-4995-bedd-7533317399cd.png)

Para el primer punto se programó el funcionamiento de cargas consistentes (que en la parte 1 de la tarea se habían ingresado las cargas manualmente), se revisó el funcionamiento para cualquier malla y esta se encuentra en el archivo "nodal_loads.py". Luego se programó el "nodal stress averaging", donde se calculó el sigma en la esquina del cuadrilátero para todos los elementos y se promediaron estas.

Para el segundo punto se utilizó la malla que se solicitaba en la Tarea 3 - Parte 1 con un total de 18264 nodos (archivo "placa_plana_a.msh"), una malla intermedia con 2546 nodos ("placa_plana_b.msh") y la malla vista en clases con 292 nodos ("placa_plana_c.msh"). A continuación se muestran los resultados obtenidos para cada malla:

Cabe destacar que la carga ingresada es de 1KN, no 1000N (para la compresión de los valores obtenidos).

MALLA a): Detallada.
![imagen](https://user-images.githubusercontent.com/81662690/126212375-74610cd4-1de5-4e2c-ab0f-2d55cc332e83.png)

Sigma xx nodal:
![imagen](https://user-images.githubusercontent.com/81662690/127943808-c64e1f48-7cab-45df-bb42-c301c4b3b6ac.png)
![imagen](https://user-images.githubusercontent.com/81662690/127943870-33cbf1f9-57b8-4386-b1c5-c1dee85269b9.png)
![imagen](https://user-images.githubusercontent.com/81662690/127943901-42630555-5a3d-4bdd-b3f7-0833b37c0e16.png)

Sigma xx por elemento:
![imagen](https://user-images.githubusercontent.com/81662690/127944009-41612b21-2be3-4e45-a10f-e7be577f01cf.png)
![imagen](https://user-images.githubusercontent.com/81662690/127943971-a5becc92-9dcd-492a-8141-71b36d20588c.png)
![imagen](https://user-images.githubusercontent.com/81662690/127943945-76c68ab2-e244-41b6-96d5-a6bef2a61cc4.png)

Desplazamiento (aplificado en 1e8):
![imagen](https://user-images.githubusercontent.com/81662690/127944096-bac70bcb-631a-4392-a692-74907a84479c.png)


MALLA b): Intermedia.
![imagen](https://user-images.githubusercontent.com/81662690/126213993-1b5447f5-5a70-4d62-b109-312f7aa710cd.png)

Sigma xx nodal:
![imagen](https://user-images.githubusercontent.com/81662690/127940670-604c5e19-2bc8-463f-984d-68fefda0b839.png)

Sigma xx por elemento:
![imagen](https://user-images.githubusercontent.com/81662690/127940709-1de12c17-18ed-452c-9861-101cc85cbae5.png)

Desplazamiento (amplificado en 1e8):
![imagen](https://user-images.githubusercontent.com/81662690/127940794-554f23c9-95d1-47f3-865b-ae1334ff678c.png)


MALLA c): Usada en clases.
![imagen](https://user-images.githubusercontent.com/81662690/126214742-596b6561-93fc-47bf-88ab-676ce26729ff.png)

Sigma xx nodal:
![imagen](https://user-images.githubusercontent.com/81662690/127943557-d7dec2c5-35eb-45ec-91fb-6535f0b181e0.png)

Sigma xx por elemento:
![imagen](https://user-images.githubusercontent.com/81662690/127943518-e0c3ff35-b934-4219-9675-58f586b2b42e.png)

Desplazamiento (amplificado en 1e8):
![imagen](https://user-images.githubusercontent.com/81662690/127943634-be3ad5ad-c280-4096-9090-c10a97452985.png)

Tercer punto:
Se graficó el refinamiento elegido para el orificio en gmsh, ya que es en este punto donde se busca mayor refinamiento y donde se concentran las tensiones máximas.
![imagen](https://user-images.githubusercontent.com/81662690/127947516-7fa70589-72d5-4cbb-a882-35a2cc04c496.png)

Al haber menor detalle de la malla, la tensión disminuye ya que se "junta" una sección más grande (toda el área del elemento) en donde la tensión en la misma por lo que el máximo va a tender a disminuir al promediarse con valores más bajos, se ven diferencias de 1 orden de magnitud entre cada malla ya que lo que se tiene para este caso es una concentración de tensiones. El problema que tiene el refinar mucho la malla es el recurso computacional utilizado aumenta.

Se puede ver claramente que el calculo de tensiones en el nodo vs en el elemento es mejor y converge más rápido, al promediarse el valor de distintos elementos es más preciso y se tienen más valores ya que son más nodos que elementos.

Para elegir la malla que es más adecuada, se debe revisar el nivel de análisis y resultados que se desea alcanzar ya que no me va a servir una malla tan refinada si me entrega resultados mucho más detallados de los que necesito, se debe optimizar el recurso computacional y tampoco usar una malla poco refinada que no me va a dar resultados correctos.

El óptimo en este caso, a mi parecer sería el refinamiento de malla que se tiene cerca del orificio para la "malla a" ya que en mi caso no demoró más de 5 minutos en ejecutarse el programa arrojando resultados nodales y de elementos.

La diferencia en desplazamientos es despreciable, aunque aumenta levemente al refinar mas y ese valor debe ser más exacto.
