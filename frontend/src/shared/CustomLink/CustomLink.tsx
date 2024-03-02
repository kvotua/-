import React, { SVGProps } from "react";
import { Link, useMatch } from "react-router-dom";

interface ICustomLink {
  Image: React.FC<SVGProps<SVGSVGElement>>;
  to?: string;
}

const CustomLink: React.FC<ICustomLink> = ({ Image, to }) => {
  const match = useMatch({ path: to ? to : "/", end: false });

  return (
    <>
      {to ? (
        <Link to={to}>
          <Image stroke={match ? "#FF78E9" : "#FFFFFF"} />
        </Link>
      ) : (
        <Image stroke={match ? "#FF78E9" : "#FFFFFF"} />
      )}
    </>
  );
};

export { CustomLink };
