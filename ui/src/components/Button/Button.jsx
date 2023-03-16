import React from "react";

const Button = ({ id, handleClick, text, type = "button" }) => {
  return (
    <button id={id} onClick={handleClick} type={type}>
      {text}
    </button>
  );
};

export default Button;
