Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const issueDiff_1 = (0, tslib_1.__importDefault)(require("app/components/issueDiff"));
const DiffModal = (_a) => {
    var { className, Body, CloseButton } = _a, props = (0, tslib_1.__rest)(_a, ["className", "Body", "CloseButton"]);
    return (<Body>
    <CloseButton />
    <issueDiff_1.default className={className} {...props}/>
  </Body>);
};
const modalCss = (0, react_1.css) `
  position: absolute;
  left: 20px;
  right: 20px;
  top: 20px;
  bottom: 20px;
  display: flex;
  padding: 0;
  width: auto;

  [role='document'] {
    overflow: scroll;
    height: 100%;
    display: flex;
    flex: 1;
  }

  section {
    display: flex;
    width: 100%;
  }
`;
exports.modalCss = modalCss;
exports.default = DiffModal;
//# sourceMappingURL=diffModal.jsx.map