const ImageUploadButton = ({ handleChooseImage, file }) => {
  return (
    <div>
      <div>{file && <img src={file} alt="oops..." />}</div>
      <label htmlFor="files">Choose Image</label>
      <input
        id="files"
        type="file"
        onChange={handleChooseImage}
        accept="image/*"
      />
    </div>
  );
};

export default ImageUploadButton;
