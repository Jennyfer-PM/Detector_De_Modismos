const ingresar = document.getElementById('ingresar');
const analizar = document.getElementById('analizar');
const resultado = document.getElementById('resultado');
const porcentaje = document.getElementById('porcentaje');
const coincidencias = document.getElementById('coincidencias');
const cambio_contenido = document.getElementById('cambio_contenido');
const cambio = document.getElementById('cambio');

let ejecucion = false;
let fragmento = 0;

analizar.addEventListener("click", () => {
    cambio_contenido.innerHTML = "";

    let resultadoD;

    const url_D = 'http://localhost:8000/detectar';
    const url_P = 'http://localhost:8000/porcentaje';
    const url_M = 'http://localhost:8000/modismo';
    const url_I = 'http://localhost:8000/indices';

    const datos = {
    texto: ingresar.value
    };

    const opciones = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    };

    async function detector() {
        try {
            const respuesta = await fetch(url_D, opciones);

            if (!respuesta.ok) {
                throw new Error(`Error en la petición: ${respuesta.status}`);
            }

            resultadoD = await respuesta.json();

            //console.log(resultadoD);

        } catch (error) {
                console.error('Hubo un problema con la petición:', error);
        }
    }

    async function cambioContenido() {
        await detector();

        if(ejecucion == true){
            const span = document.getElementById("newe");
            if (span) {
                span.remove();
            }
        }
        porcentaje.innerHTML = '';
        coincidencias.innerHTML = '';
        resultado.innerHTML = '';
        cambio.innerHTML = '';
        //console.log(resultadoD);
        if (resultadoD == true) {
            cambio.innerHTML = `
                <br>
                <p class='texto'>Detección del modismo:</p>
            `;
            try {
                const respuesta = await fetch(url_P, opciones);

                if (!respuesta.ok) {
                    throw new Error(`Error en la petición: ${respuesta.status}`);
                }

                const resultadoB = await respuesta.json();

                if (resultadoB != 0) {
                    porcentaje.innerHTML = "Coincidencia con modismos del: " + resultadoB + "%";
                }

            } catch (error) {
                console.error('Hubo un problema con la petición:', error);
            }
        

            try {
                const respuesta = await fetch(url_M, opciones);

                if (!respuesta.ok) {
                    throw new Error(`Error en la petición: ${respuesta.status}`);
                }

                const resF = await respuesta.json();

                if (resF.length == 1) {
                    resultado.innerHTML = "Se encontro el siguiente modismo: " + resF;
                } else {
                    resultado.innerHTML = "Se encontraron los siguientes modismos: " + resF;
                }

            } catch (error) {
                console.error('Hubo un problema con la petición:', error);
            }

            try {
                const respuesta = await fetch(url_I, opciones);

                if (!respuesta.ok) {
                    throw new Error(`Error en la petición: ${respuesta.status}`);
                }

                const resultadoA = await respuesta.json();

                //console.log(resultadoA)

                texto = ingresar.value.split(" ");

                finalM = resultadoA.length

                ultimo = texto.length

                for (let i = 0; i < finalM; i++) {
                    if (resultadoA[i][0] == 0 && resultadoA[i][1] == (texto.length - 1)) {
                        var nuevo = document.createElement("span");
                        nuevo.id = "newe";
                        console.log('entre a este if 1')
                        nuevo.innerHTML = `
                        <mark class='textoR'>${ingresar.value}</mark>
                        `;
                        cambio.appendChild(nuevo)
                    } else if (resultadoA[i][0] == 0) {
                        var nuevo = document.createElement("span");
                        nuevo.id = "newe";
                        console.log('entre a este if 2')
                        indice1 = resultadoA[0][1] + 1
                        uno = (texto.slice(0, indice1)).join(" ");
                        if (finalM != 1) {
                            nuevo.innerHTML = `
                                <mark class='textoR'>${uno}</mark>
                            `;
                        } else {
                            dos = (texto.slice(indice1, ultimo)).join(" ");
                            nuevo.innerHTML = `
                                <mark class='textoR'>${uno}</mark>
                                <span class='textoR'>${dos}</span>
                            `;
                        }
                        cambio.appendChild(nuevo)
                    } else if (resultadoA[i][1] == (ultimo - 1)) {
                        //console.log(resultadoA);
                        console.log(texto)
                        var nuevo = document.createElement("span");
                        nuevo.id = "newe";
                        console.log('entre a este otro if 3')
                        if (i == 0){
                            indice1 = resultadoA[0][0];
                        } else if (i < 2) {
                            indice1 = resultadoA[i][0] - frag;
                        } else {
                            indice1 = resultadoA[i][0] - frag - 2;
                        }
                        uno = (texto.slice(0, indice1)).join(" ");
                        dos = (texto.slice(indice1, ultimo)).join(" ");
                        nuevo.innerHTML = `
                        <span class='textoR'>${uno}</span>
                        <mark class='textoR'>${dos}</mark>
                        `;
                        cambio.appendChild(nuevo)
                    } else {
                        var nuevo = document.createElement("span");
                        nuevo.id = "newe";
                        console.log('entre a este if 4')
                        if (i > 0) {
                            indice1 = resultadoA[i][0] - frag;
                            indice2 = resultadoA[i][1] - frag + 1;
                        } else {
                            indice1 = resultadoA[i][0];
                            indice2 = resultadoA[i][1] + 1;
                        }
                        uno = (texto.slice(0, indice1)).join(" ");
                        dos = (texto.slice(indice1, indice2)).join(" ");
                        if (i < finalM) {
                            tres = (texto.slice(indice2).join(" "));
                        } else {
                            tres = (texto.slice(indice2, ultimo)).join(" ");
                        }
                        if (i == 0 && finalM == 1) {
                            nuevo.innerHTML = `
                                <span class='textoR'>${uno}</span>
                                <mark class='textoR'>${dos}</mark>
                                <span class='textoR'>${tres}</span>
                                `;
                        } else if (i < (finalM - 1)) {
                            nuevo.innerHTML = `
                                <span class='textoR'>${uno}</span>
                                <mark class='textoR'>${dos}</mark>
                                `;
                        } else {
                            nuevo.innerHTML = `
                                <span class='textoR'>${uno}</span>
                                <mark class='textoR'>${dos}</mark>
                                <span class='textoR'>${tres}</span>
                            `;
                        }
                        cambio.appendChild(nuevo)
                    }

                    particion = (resultadoA[i][1]);
                    cuenta = (resultadoA[i][0])
                    if (cuenta == 0){
                        parte = texto.slice(cuenta, particion + 1);
                    } else {
                        parte = texto.slice(cuenta - 1, particion + 1);
                    }

                    let conta = texto.slice(0, cuenta)
                    frag = parte.length;

                    if (i < 1) {
                        texto = texto.slice(particion + 1, ultimo);
                    } else {
                        texto = texto.slice(particion - frag + 1, ultimo - frag)
                        fragmento = fragmento + frag;
                        frag = fragmento - 1;
                    }

                    fragmento = frag;
                }

                ejecucion = true;

            } catch (error) {
                console.error('Hubo un problema con la petición:', error);
            }
        } else {
            cambio_contenido.innerHTML = `
                <p class='texto'>NO SE DETECTO NINGÚN MODISMO</p>
            `;
            porcentaje.innerHTML = '';
            coincidencias.innerHTML = '';
            resultado.innerHTML = '';
        }
    }

    cambioContenido();
})