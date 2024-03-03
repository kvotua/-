import React from "react";

interface IAddButton {
  handleClick?: (event: unknown) => void;
}
const AddButton: React.FC<IAddButton> = ({ handleClick }) => {
  return (
    <button
      onClick={handleClick}
      className="px-4 py-8 border-2 border-dashed border-black w-full h-full text-4xl rounded-20 duration-200"
    >
      +
    </button>
  );
};

export { AddButton };
