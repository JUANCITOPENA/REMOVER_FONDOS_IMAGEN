import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import time

def enhance_image(image):
    """Mejora el contraste de la imagen para optimizar la eliminación del fondo."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5)

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

                st.session_state.processed_image = img_no_bg  # Guardar en session_state

                # Ocultar el progreso
                progress_bar.empty()
                status_text.markdown('<div class="green-bg">Procesamiento completado.</div>', unsafe_allow_html=True)

                # Mostrar imágenes
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

        # Convertir imagen a bytes para la descarga
        img_bytes_io = io.BytesIO()
        img_format = "PNG" if format_option == "PNG" else "JPEG"
        st.session_state.processed_image.save(img_bytes_io, format=img_format)
        img_bytes_io.seek(0)

        st.download_button(
            label="Descargar imagen sin fondo",
            data=img_bytes_io,
            file_name=f"imagen_sin_fondo.{format_option.lower()}",
            mime=f"image/{format_option.lower()}"
        )

        # Botón para limpiar
        if st.button("🔄 Limpiar y comenzar de nuevo"):
            st.session_state.processed_image = None
            st.session_state.image = None
            st.session_state.uploaded_file_name = None
            st.rerun()

if __name__ == "__main__":
    main()
