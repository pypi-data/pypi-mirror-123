Object.defineProperty(exports, "__esModule", { value: true });
exports.ModalFooter = exports.ModalBody = exports.makeCloseButton = exports.makeClosableHeader = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ModalHeader = (0, styled_1.default)('header') `
  position: relative;
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)};
  margin: -${(0, space_1.default)(4)} -${(0, space_1.default)(4)} ${(0, space_1.default)(3)} -${(0, space_1.default)(4)};

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 0;
    line-height: 1.1;
  }
`;
const CloseButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(50%, -50%);
  border-radius: 50%;
  background: ${p => p.theme.background};
  height: 24px;
  width: 24px;
`;
CloseButton.defaultProps = {
    label: (0, locale_1.t)('Close Modal'),
    icon: <iconClose_1.IconClose size="10px"/>,
    size: 'zero',
};
const ModalBody = (0, styled_1.default)('section') `
  font-size: 15px;

  p:last-child {
    margin-bottom: 0;
  }

  img {
    max-width: 100%;
  }
`;
exports.ModalBody = ModalBody;
const ModalFooter = (0, styled_1.default)('footer') `
  border-top: 1px solid ${p => p.theme.border};
  display: flex;
  justify-content: flex-end;
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)};
  margin: ${(0, space_1.default)(3)} -${(0, space_1.default)(4)} -${(0, space_1.default)(4)};
`;
exports.ModalFooter = ModalFooter;
/**
 * Creates a ModalHeader that includes props to enable the close button
 */
const makeClosableHeader = (closeModal) => {
    const ClosableHeader = (_a) => {
        var { closeButton, children } = _a, props = (0, tslib_1.__rest)(_a, ["closeButton", "children"]);
        return (<ModalHeader {...props}>
        {children}
        {closeButton && <CloseButton onClick={closeModal}/>}
      </ModalHeader>);
    };
    ClosableHeader.displayName = 'Header';
    return ClosableHeader;
};
exports.makeClosableHeader = makeClosableHeader;
/**
 * Creates a CloseButton component that is connected to the provided closeModal trigger
 */
const makeCloseButton = (closeModal) => props => <CloseButton {...props} onClick={closeModal}/>;
exports.makeCloseButton = makeCloseButton;
//# sourceMappingURL=components.jsx.map