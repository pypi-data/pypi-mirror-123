Object.defineProperty(exports, "__esModule", { value: true });
exports.inputStyles = exports.INPUT_PADDING = void 0;
const react_1 = require("@emotion/react");
exports.INPUT_PADDING = 10;
const inputStyles = (props) => (0, react_1.css) `
    color: ${props.disabled ? props.theme.disabled : props.theme.formText};
    display: block;
    width: 100%;
    background: ${props.theme.background};
    border: 1px solid ${props.theme.border};
    border-radius: ${props.theme.borderRadius};
    box-shadow: inset ${props.theme.dropShadowLight};
    padding: ${exports.INPUT_PADDING}px;
    transition: border 0.1s linear;
    resize: vertical;
    height: 40px;

    ${props.monospace ? `font-family: ${props.theme.text.familyMono}` : ''};

    ${props.readOnly
    ? (0, react_1.css) `
          cursor: default;
        `
    : ''};

    &:focus {
      outline: none;
    }

    &:hover,
    &:focus,
    &:active {
      border: 1px solid ${props.theme.border};
    }

    &::placeholder {
      color: ${props.theme.formPlaceholder};
    }

    &[disabled] {
      background: ${props.theme.backgroundSecondary};
      color: ${props.theme.gray300};
      border: 1px solid ${props.theme.border};
      cursor: not-allowed;

      &::placeholder {
        color: ${props.theme.disabled};
      }
    }

    &.focus-visible {
      box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;
    }
  `;
exports.inputStyles = inputStyles;
//# sourceMappingURL=input.jsx.map