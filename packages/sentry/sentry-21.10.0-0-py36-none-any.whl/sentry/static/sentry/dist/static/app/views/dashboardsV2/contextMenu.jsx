Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const icons_1 = require("app/icons");
const ContextMenu = ({ children }) => (<dropdownMenu_1.default>
    {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
        const topLevelCx = (0, classnames_1.default)('dropdown', {
            'anchor-right': true,
            open: isOpen,
        });
        return (<MoreOptions {...getRootProps({
            className: topLevelCx,
        })}>
          <DropdownTarget {...getActorProps({
            onClick: (event) => {
                event.stopPropagation();
                event.preventDefault();
            },
        })}>
            <icons_1.IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={(0, classnames_1.default)('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
    }}
  </dropdownMenu_1.default>);
const MoreOptions = (0, styled_1.default)('span') `
  display: flex;
  color: ${p => p.theme.textColor};
`;
const DropdownTarget = (0, styled_1.default)('div') `
  display: flex;
  cursor: pointer;
  padding: 0 5px;
`;
exports.default = ContextMenu;
//# sourceMappingURL=contextMenu.jsx.map