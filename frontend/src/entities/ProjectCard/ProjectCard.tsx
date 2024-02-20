import React from "react";
import Edit from "../../assets/icons/edit.svg?react";
import Link from "../../assets/icons/link.svg?react";

interface IProjectCard {
  title: string;
}

const ProjectCard: React.FC<IProjectCard> = ({ title }) => {
  return (
    <div className="bg-main rounded-20 h-[280px] text-center p-[20px] flex flex-col justify-between">
      <h2 className="text-[practice20px] font-bold">{title}</h2>
      <div className="flex justify-between">
        <Edit stroke="black" />
        <Link fill="black" />
      </div>
    </div>
  );
};

export { ProjectCard };
