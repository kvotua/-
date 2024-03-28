import React from "react";
import { type IAddButton } from "./AddButtonModel";
import { motion } from "framer-motion";

const AddButton: React.FC<IAddButton> = ({ handleClick }) => {
  return (
    <motion.button
      onClick={handleClick}
      className="px-4 py-8 border-2 border-dashed border-black w-full h-full text-4xl rounded-20 duration-200"
    >
      +
    </motion.button>
  );
};

export { AddButton };
