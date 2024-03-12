import React from "react";
import { Outlet } from "react-router-dom";
import { motion } from "framer-motion";

import { CustomLink } from "src/shared/CustomLink/CustomLink";
import style from "./menu.module.css";

interface IMenu {
  link?: string;
  Image: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  handleClick?: (n: unknown) => void;
}

interface IMenuItem {
  menuItem: IMenu[];
}

const Menu: React.FC<IMenuItem> = ({ menuItem }) => {
  console.log("render");

  return (
    <>
      <Outlet />
      <div className="container">
        <motion.nav className={style.menu}>
          <ul className="flex justify-between gap-[8vw]">
            {menuItem.map(({ link, Image, handleClick }, i) => (
              <li key={i} onClick={handleClick}>
                <CustomLink to={link} Image={Image} />
              </li>
            ))}
          </ul>
        </motion.nav>
      </div>
    </>
  );
};

export { Menu };
