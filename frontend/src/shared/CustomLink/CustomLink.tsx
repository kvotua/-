import React, { SVGProps } from "react";
import { Link, useLocation, useMatch } from "react-router-dom";

interface ICustomLink {
  Image: React.FC<SVGProps<SVGSVGElement>>;
  to?: string;
}

const CustomLink: React.FC<ICustomLink> = ({ Image, to }) => {
  const match = useMatch({ path: to ? to : "/", end: false });
  const location = useLocation();

  return (
    <>
      {to ? (
        <Link to={to}>
          <Image
            stroke={
              match?.pathname === "/"
                ? location.pathname === match.pathname
                  ? "#FF78E9"
                  : "white"
                : match
                  ? "#FF78E9"
                  : "white"
            }
          />
        </Link>
      ) : (
        <Image
          stroke={
            match?.pathname === "/"
              ? location.pathname === match.pathname
                ? "#FF78E9"
                : "white"
              : match
                ? "#FF78E9"
                : "white"
          }
        />
      )}
    </>
  );
};

export { CustomLink };
