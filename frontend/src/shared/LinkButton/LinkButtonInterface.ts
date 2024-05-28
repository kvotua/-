export interface ILinkButtonProps {
  title: string | undefined;
  buttonActive: boolean;
  handleClick?: () => void;
  type: string;
}
