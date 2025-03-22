import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import time
import base64

def enhance_image(image):
    """Mejora el contraste de la imagen para optimizar la eliminación del fondo."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5)

def get_download_link(img_bytes, format_option):
    """
    Genera un enlace HTML para descargar la imagen.
    Se usa la codificación base64 para incrustar la imagen y un onClick
    para recargar la página tras la descarga.
    """
    b64 = base64.b64encode(img_bytes).decode()
    filename = f"imagen_sin_fondo.{format_option.lower()}"
    # El script onClick recarga la página después de 100ms
    href = (
        f"<a href='data:image/{format_option.lower()};base64,{b64}' "
        f"download='{filename}' "
        f"onClick=\"setTimeout(() => window.location.reload(), 100)\">"
        f"Descargar imagen sin fondo</a>"
    )
    return href

def main():
    st.title("🖼️ REMOVER FONDO DE IMÁGENES ✂️")

    st.markdown(
        "<h4 style='text-align: center; color: gray;'>Creado por Juancito Peña</h4>",
        unsafe_allow_html=True
    )

    # CSS personalizado
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
    if "processed_image" not in st.session_state:
        st.session_state.processed_image = None
        st.session_state.image = None
        st.session_state.uploaded_file_name = None

    uploaded_file = st.file_uploader("Elige un archivo de imagen (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            # Si se carga una imagen nueva, se procesa
            if st.session_state.uploaded_file_name != uploaded_file.name:
                image = Image.open(uploaded_file).convert("RGBA")
                st.session_state.image = image
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.processed_image = None  

                enhanced_image = enhance_image(image)

                # Simular progreso
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(0, 100, 20):
                    time.sleep(0.3)
                    progress_bar.progress(percent_complete)
                    status_text.text(f"Procesando... {percent_complete}%")

                # Convertir imagen mejorada a bytes
                img_byte_arr = io.BytesIO()
                enhanced_image.save(img_byte_arr, format="PNG")
                img_bytes = img_byte_arr.getvalue()

                # Remover fondo
                result_bytes = remove(img_bytes)

                # Convertir la imagen resultante
                img_no_bg = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

                st.session_state.processed_image = img_no_bg

                # Ocultar el progreso
                progress_bar.empty()
                status_text.markdown('<div class="green-bg">Procesamiento completado.</div>', unsafe_allow_html=True)

                # Mostrar imágenes originales y procesadas
                col1, col2 = st.columns(2)
                with col1:
                    st.header("Imagen original")
                    st.image(image, caption="Imagen original", use_container_width=True)
                with col2:
                    st.header("Imagen sin fondo")
                    st.image(img_no_bg, caption="Imagen sin fondo", use_container_width=True)

        except Exception as e:
            st.error(f"Error al procesar la imagen: {e}")

    if st.session_state.processed_image is not None:
        st.markdown("### Selecciona el formato de descarga")
        format_option = st.selectbox("Formato", ["PNG", "JPEG"])

        # Convertir imagen a bytes según el formato seleccionado
        img_bytes_io = io.BytesIO()
        img_format = "PNG" if format_option == "PNG" else "JPEG"
        st.session_state.processed_image.save(img_bytes_io, format=img_format)
        img_bytes = img_bytes_io.getvalue()

        # Mostrar enlace de descarga que recarga la página al hacer clic
        download_link = get_download_link(img_bytes, format_option)
        st.markdown(download_link, unsafe_allow_html=True)

        # También se ofrece un botón alternativo para limpiar manualmente
        if st.button("🔄 Limpiar y comenzar de nuevo"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
