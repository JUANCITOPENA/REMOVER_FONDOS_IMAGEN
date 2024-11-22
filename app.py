import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import time
import onnxruntime as ort

def enhance_image(image):
    # Mejorar la imagen antes de procesarla para mejor precisión
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Aumentar el contraste
    return image

def main():
    st.title("🖼️ REMOVER FONDO DE IMÁGENES ✂️")

    # Subtítulo
    st.markdown(
        """
        <h4 style='text-align: center; color: gray;'>Creado por Juancito Peña</h4>
        """,
        unsafe_allow_html=True
    )

    # CSS personalizado para cambiar el fondo y estilo del texto
    st.markdown(
        """
        <style>
        .green-bg {
            background-color: #28a745;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializar el estado de sesión
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None
        st.session_state.image = None
        st.session_state.uploaded_file_name = None
        st.session_state.processing = False

    # Subir la imagen
    uploaded_file = st.file_uploader("Elige un archivo de imagen (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            # Verificar si el archivo es diferente al anterior
            if st.session_state.uploaded_file_name != uploaded_file.name:
                # Cargar la imagen subida
                image = Image.open(uploaded_file)
                st.session_state.image = image
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.processed_image = None  # Reiniciar imagen procesada

                # Mejorar la imagen antes de remover el fondo
                enhanced_image = enhance_image(image)

                # Mostrar un indicador de progreso
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Simular el progreso mientras se procesa la imagen
                st.session_state.processing = True
                for percent_complete in range(0, 101, 20):
                    time.sleep(0.5)  # Simulación de tiempo de proceso
                    progress_bar.progress(percent_complete)
                    status_text.text(f"Procesando... {percent_complete}%")

                # Convertir la imagen mejorada a bytes
                img_byte_arr = io.BytesIO()
                enhanced_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                # Remover el fondo
                result = remove(img_byte_arr)

                # Guardar el resultado en session_state
                st.session_state.processed_image = result

                # Convertir el resultado a imagen
                img_no_bg = Image.open(io.BytesIO(result))

                # Mostrar las imágenes
                col1, col2 = st.columns(2)
                with col1:
                    st.header("Imagen original")
                    st.image(image, caption="Imagen original", use_column_width=True)

                with col2:
                    st.header("Imagen sin fondo")
                    st.image(img_no_bg, caption="Imagen sin fondo", use_column_width=True)

                # Ocultar el texto y barra de progreso al finalizar
                progress_bar.empty()
                status_text.markdown('<div class="green-bg">Procesamiento completado.</div>', unsafe_allow_html=True)
                st.session_state.processing = False
        except Exception as e:
            st.error(f"Error al procesar la imagen: {e}")

    if st.session_state.processed_image is not None:
        # Opciones de formato de descarga
        st.markdown("### Selecciona el formato de descarga")
        format_option = st.selectbox("Formato", ["PNG", "JPEG"])

        # Botón para descargar la imagen sin fondo
        download_format = "image/png" if format_option == "PNG" else "image/jpeg"
        st.download_button(
            label="Descargar imagen sin fondo",
            data=st.session_state.processed_image,
            file_name=f"imagen_sin_fondo.{format_option.lower()}",
            mime=download_format
        )

if __name__ == "__main__":
    main()
 