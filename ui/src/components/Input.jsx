import React from "react";

const Input = ({
  id,
  name,
  type = "text",
  placeholder,
  value,
  onBlur,
  onChange,
  error,
}) => {
  return (
    <input
      id={id}
      name={name}
      type={type}
      placeholder={placeholder}
      value={value}
      onBlur={onBlur}
      onChange={onChange}
      style={{ borderColor: error ? "#ff59a7" : undefined }}
    />
  );
};

export default Input;
