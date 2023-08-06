Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("@emotion/react");
const SidebarDropdownMenu = (p) => (0, react_1.css) `
  position: absolute;
  background: ${p.theme.background};
  color: ${p.theme.textColor};
  border-radius: 4px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08), 0 4px 20px 0 rgba(0, 0, 0, 0.3);
  padding: 5px 0;
  width: 250px;
  z-index: 1000;
`;
exports.default = SidebarDropdownMenu;
//# sourceMappingURL=sidebarDropdownMenu.styled.jsx.map