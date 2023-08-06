Object.defineProperty(exports, "__esModule", { value: true });
exports.MergedStyles = exports.ButtonGrid = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const button_1 = require("app/components/button");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function ButtonBar({ children, className, active, merged = false, gap = 0, }) {
    const shouldCheckActive = typeof active !== 'undefined';
    return (<ButtonGrid merged={merged} gap={gap} className={className}>
      {!shouldCheckActive
            ? children
            : React.Children.map(children, child => {
                if (!React.isValidElement(child)) {
                    return child;
                }
                const { props: childProps } = child, childWithoutProps = (0, tslib_1.__rest)(child, ["props"]);
                // We do not want to pass `barId` to <Button>`
                const { barId } = childProps, props = (0, tslib_1.__rest)(childProps, ["barId"]);
                const isActive = active === barId;
                // This ["primary"] could be customizable with a prop,
                // but let's just enforce one "active" type for now
                const priority = isActive ? 'primary' : childProps.priority || 'default';
                return React.cloneElement(childWithoutProps, Object.assign(Object.assign({}, props), { className: (0, classnames_1.default)(className, { active: isActive }), priority }));
            })}
    </ButtonGrid>);
}
const MergedStyles = () => (0, react_1.css) `
  /* Raised buttons show borders on both sides. Useful to create pill bars */
  & > .active {
    z-index: 2;
  }

  & > .dropdown,
  & > button,
  & > input,
  & > a {
    position: relative;

    /* First button is square on the right side */
    &:first-child:not(:last-child) {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;

      & > .dropdown-actor > ${button_1.StyledButton} {
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
      }
    }

    /* Middle buttons are square */
    &:not(:last-child):not(:first-child) {
      border-radius: 0;

      & > .dropdown-actor > ${button_1.StyledButton} {
        border-radius: 0;
      }
    }

    /* Middle buttons only need one border so we don't get a double line */
    &:first-child {
      & + .dropdown:not(:last-child),
      & + a:not(:last-child),
      & + input:not(:last-child),
      & + button:not(:last-child) {
        margin-left: -1px;
      }
    }

    /* Middle buttons only need one border so we don't get a double line */
    /* stylelint-disable-next-line no-duplicate-selectors */
    &:not(:last-child):not(:first-child) {
      & + .dropdown,
      & + button,
      & + input,
      & + a {
        margin-left: -1px;
      }
    }

    /* Last button is square on the left side */
    &:last-child:not(:first-child) {
      border-top-left-radius: 0;
      border-bottom-left-radius: 0;
      margin-left: -1px;

      & > .dropdown-actor > ${button_1.StyledButton} {
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
        margin-left: -1px;
      }
    }
  }
`;
exports.MergedStyles = MergedStyles;
const ButtonGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-column-gap: ${p => (0, space_1.default)(p.gap)};
  align-items: center;

  ${p => p.merged && MergedStyles}
`;
exports.ButtonGrid = ButtonGrid;
exports.default = ButtonBar;
//# sourceMappingURL=buttonBar.jsx.map