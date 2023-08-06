Object.defineProperty(exports, "__esModule", { value: true });
exports.openConfirmModal = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
/**
 * Opens a confirmation modal when called. The procedural version of the
 * `Confirm` component
 */
const openConfirmModal = (_a) => {
    var _b;
    var { bypass, onConfirming, priority = 'primary', cancelText = (0, locale_1.t)('Cancel'), confirmText = (0, locale_1.t)('Confirm'), disableConfirmButton = false } = _a, rest = (0, tslib_1.__rest)(_a, ["bypass", "onConfirming", "priority", "cancelText", "confirmText", "disableConfirmButton"]);
    if (bypass) {
        (_b = rest.onConfirm) === null || _b === void 0 ? void 0 : _b.call(rest);
        return;
    }
    const modalProps = Object.assign(Object.assign({}, rest), { priority,
        confirmText,
        cancelText,
        disableConfirmButton });
    onConfirming === null || onConfirming === void 0 ? void 0 : onConfirming();
    (0, modal_1.openModal)(renderProps => <ConfirmModal {...renderProps} {...modalProps}/>);
};
exports.openConfirmModal = openConfirmModal;
/**
 * The confirm component is somewhat special in that you can wrap any
 * onClick-able element with this to trigger a interstital confirmation modal.
 *
 * This is the declarative alternative to using openConfirmModal
 */
function Confirm(_a) {
    var { disabled, children, stopPropagation = false } = _a, openConfirmOptions = (0, tslib_1.__rest)(_a, ["disabled", "children", "stopPropagation"]);
    const triggerModal = (e) => {
        if (stopPropagation) {
            e === null || e === void 0 ? void 0 : e.stopPropagation();
        }
        if (disabled) {
            return;
        }
        (0, exports.openConfirmModal)(openConfirmOptions);
    };
    if (typeof children === 'function') {
        return children({ open: triggerModal });
    }
    if (!React.isValidElement(children)) {
        return null;
    }
    // TODO(ts): Understand why the return type of `cloneElement` is strange
    return React.cloneElement(children, { disabled, onClick: triggerModal });
}
class ConfirmModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            disableConfirmButton: !!this.props.disableConfirmButton,
            confirmCallback: null,
        };
        this.confirming = false;
        this.handleClose = () => {
            const { disableConfirmButton, onCancel, closeModal } = this.props;
            onCancel === null || onCancel === void 0 ? void 0 : onCancel();
            this.setState({ disableConfirmButton: disableConfirmButton !== null && disableConfirmButton !== void 0 ? disableConfirmButton : false });
            // always reset `confirming` when modal visibility changes
            this.confirming = false;
            closeModal();
        };
        this.handleConfirm = () => {
            var _a, _b;
            const { onConfirm, closeModal } = this.props;
            // `confirming` is used to ensure `onConfirm` or the confirm callback is
            // only called once
            if (!this.confirming) {
                onConfirm === null || onConfirm === void 0 ? void 0 : onConfirm();
                (_b = (_a = this.state).confirmCallback) === null || _b === void 0 ? void 0 : _b.call(_a);
            }
            this.setState({ disableConfirmButton: true });
            this.confirming = true;
            closeModal();
        };
    }
    get confirmMessage() {
        const { message, renderMessage } = this.props;
        if (typeof renderMessage === 'function') {
            return renderMessage({
                confirm: this.handleConfirm,
                close: this.handleClose,
                disableConfirmButton: (state) => this.setState({ disableConfirmButton: state }),
                setConfirmCallback: (confirmCallback) => this.setState({ confirmCallback }),
            });
        }
        if (React.isValidElement(message)) {
            return message;
        }
        return (<p>
        <strong>{message}</strong>
      </p>);
    }
    render() {
        const { Header, Body, Footer, priority, confirmText, cancelText, header, renderConfirmButton, renderCancelButton, } = this.props;
        return (<React.Fragment>
        {header && <Header>{header}</Header>}
        <Body>{this.confirmMessage}</Body>
        <Footer>
          <buttonBar_1.default gap={2}>
            {renderCancelButton ? (renderCancelButton({
                closeModal: this.props.closeModal,
                defaultOnClick: this.handleClose,
            })) : (<button_1.default onClick={this.handleClose}>{cancelText}</button_1.default>)}
            {renderConfirmButton ? (renderConfirmButton({
                closeModal: this.props.closeModal,
                defaultOnClick: this.handleConfirm,
            })) : (<button_1.default data-test-id="confirm-button" disabled={this.state.disableConfirmButton} priority={priority} onClick={this.handleConfirm} autoFocus>
                {confirmText}
              </button_1.default>)}
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    }
}
exports.default = Confirm;
//# sourceMappingURL=confirm.jsx.map