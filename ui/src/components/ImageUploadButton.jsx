const ImageUploadButton = ({ handleChooseImage, url }) => {
  return (
    <div>
      <div>{url && <img src={url} alt="oops..." />}</div>
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
