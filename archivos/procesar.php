<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $cedula = $_POST['cedula'];
    $encontrado = false;
    $nombre = '';
    $apellido = '';

    // Leer el archivo Estudiantes.txt
    $archivoEstudiantes = fopen("estudiantes.txt", "r");

    while (($linea = fgets($archivoEstudiantes)) !== false) {
        list($cedulaEstudiante, $nombreEstudiante, $apellidoEstudiante) = explode(",", trim($linea));

        if ($cedula == $cedulaEstudiante) {
            $nombre = $nombreEstudiante;
            $apellido = $apellidoEstudiante;
            $encontrado = true;
            break;
        }
    }

    fclose($archivoEstudiantes);

    if ($encontrado) {
        // Registrar la entrada/salida en el archivo Ingresos.txt
        $fecha = date("Y-m-d");
        $horaModificada = date("H:i", strtotime('-7 hours'));
        $tipoRegistro = "ENTRADA"; // Valor por defecto si no hay registros anteriores

        // Leer el archivo Ingresos.txt para buscar registros del día actual
        $archivoIngresos = fopen("ingresos.txt", "r");

        $ultimoRegistro = null; // Para guardar el último tipoRegistro del estudiante en el día actual

        while (($linea = fgets($archivoIngresos)) !== false) {
            list($cedulaRegistro, $fechaRegistro, $horaRegistro, $tipoRegistroRegistro) = explode(",", trim($linea));

            if ($cedula == $cedulaRegistro && $fecha == $fechaRegistro) {
                $ultimoRegistro = $tipoRegistroRegistro; // Guardar el último tipoRegistro encontrado
            }
        }

        fclose($archivoIngresos);

        // Si se encuentra un último registro en el día actual, cambiar el tipo de registro
        if ($ultimoRegistro) {
            if ($ultimoRegistro == "ENTRADA") {
                $tipoRegistro = "SALIDA";
                $mensaje = "ADIOS $nombre $apellido";
            } else {
                $tipoRegistro = "ENTRADA";
                $mensaje = "BIENVENIDO(A) $nombre $apellido";
            }
        } else {
            // Si no hay registros anteriores, se asume entrada
            $tipoRegistro = "ENTRADA";
            $mensaje = "BIENVENIDO(A) $nombre $apellido";
        }

        // Registrar la entrada/salida en el archivo Ingresos.txt
        $registro = "$cedula,$fecha,$horaModificada,$tipoRegistro\n";
        $archivoIngresos = fopen("ingresos.txt", "a");
        fwrite($archivoIngresos, $registro);
        fclose($archivoIngresos);

        // Devolver el mensaje de éxito
        echo json_encode(['mensaje' => $mensaje]);
    } else {
        // Devolver el mensaje de error
        echo json_encode(['mensaje' => "Estudiante no encontrado."]);
    }
}
?>