Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const Modal = ({ title, onSave, content, disabled, Header, Body, Footer, closeModal, btnSaveLabel = (0, locale_1.t)('Save'), }) => (<React.Fragment>
    <Header closeButton>{title}</Header>
    <Body>{content}</Body>
    <Footer>
      <buttonBar_1.default gap={1.5}>
        <button_1.default onClick={closeModal}>{(0, locale_1.t)('Cancel')}</button_1.default>
        <button_1.default onClick={event => {
        event.preventDefault();
        onSave();
    }} disabled={disabled} type="submit" priority="primary" form="relay-form">
          {btnSaveLabel}
        </button_1.default>
      </buttonBar_1.default>
    </Footer>
  </React.Fragment>);
exports.default = Modal;
//# sourceMappingURL=modal.jsx.map