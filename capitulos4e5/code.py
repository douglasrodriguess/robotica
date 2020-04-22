# Capítulos 4 e 5 - Arquiteturas de Controle

# Objetivo: observar o robô desviando de obstáculos

# Bibliotecas
from controller import Robot
from controller import Motor
from controller import DistanceSensor

# Definindo as variáveis

maxSpeed = 12.00 # Velocidade máxima
spedTime = 64   # Tempo de passo da simulação
distanceMax = 30 # Distancia máxima do robô para o obstáculo

# Inicializa o robô

robo = Robot()

# Nomeia as variávies para cada motor do Pioneer 3-AT.
# Fonte: https://cyberbotics.com/doc/guide/pioneer-3at

frontRightWheel = robo.getMotor('front right wheel')
frontLeftWheel = robo.getMotor('front left wheel')
backRightWheel = robo.getMotor('back right wheel')
backLeftWheel = robo.getMotor('back left wheel')

# Para exemplificar, definimos o destino como infinito

frontRightWheel.setPosition(float('inf'))
frontLeftWheel.setPosition(float('inf'))
backRightWheel.setPosition(float('inf'))
backLeftWheel.setPosition(float('inf'))

# Inicializando os sensores
# Sensores utilizados: so0, so1, so2, so3, so4, so5, so6, so7
# O ângulo entre duas direções consecutivas do sensor é de 20 graus, exceto para os quatro
# sensores laterais (so0, so7) nos quais o ângulo é de 40 graus.

sonarSensors = ['so0', 'so1', 'so2', 'so3', 'so4', 'so5', 'so6', 'so7']

sensorsVet = []
for aux in range(0, len(sonarSensors)):
    sensorsVet.append(robo.getDistanceSensor(sonarSensors[aux]))
    sensorsVet[aux].enable(spedTime)

# Segunda leitura em diante...

while robo.step(spedTime) !=-1:
    sensorsValues = []
    for aux in range(0, len(sonarSensors)):
        sensorsValues.append(sensorsVet[aux].getValue())

    rightObstacle = sensorsValues[0] > distanceMax or sensorsValues[1] > distanceMax or sensorsValues[2] > distanceMax
    leftObstacle = sensorsValues[5] > distanceMax or sensorsValues[6] > distanceMax or sensorsValues[7] > distanceMax
    frontObstacle = sensorsValues[3] > (distanceMax-20) or sensorsValues[4] > (distanceMax-20)

    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed = 0.3 * maxSpeed
    rightSpeed = 0.3 * maxSpeed

    # modify speeds according to obstacles
    if frontObstacle:
        leftSpeed += 0.3 * maxSpeed
        rightSpeed += 0.3 * maxSpeed
    elif leftObstacle:
        leftSpeed -= 0.3 * maxSpeed
        rightSpeed += 0.3 * maxSpeed
    elif rightObstacle:
        leftSpeed += 0.3 * maxSpeed
        rightSpeed -= 0.3 * maxSpeed

    # set up the motor speeds at x% of the MAX_SPEED.
    frontLeftWheel.setVelocity(leftSpeed)
    frontRightWheel.setVelocity(rightSpeed)
    backLeftWheel.setVelocity(leftSpeed)
    backRightWheel.setVelocity(rightSpeed)

    pass
