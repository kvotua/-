import React from "react";
import Edit from "../../assets/icons/edit.svg?react";
import LinkIcon from "../../assets/icons/link.svg?react";
import { Link } from "react-router-dom";

interface IProjectCard {
  title: string;
  id: string;
}

const ProjectCard: React.FC<IProjectCard> = ({ title, id }) => {
  return (
    <Link
      to={`/project/${id}`}
      className="bg-main rounded-20 text-center p-[20px] flex flex-col justify-between min-h-[60dvh]"
    >
      <h2 className="text-[practice20px] font-bold">{title}</h2>
      <div className="flex justify-between">
        <Link to={`/project/${id}/edit`}>
          <Edit stroke="black" />
        </Link>
        <LinkIcon fill="black" />
      </div>
    </Link>
  );
};

export { ProjectCard };
