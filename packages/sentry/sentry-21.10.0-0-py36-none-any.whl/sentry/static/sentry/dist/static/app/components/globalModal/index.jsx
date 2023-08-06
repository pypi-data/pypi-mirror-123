Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const focus_trap_1 = require("focus-trap");
const framer_motion_1 = require("framer-motion");
const modal_1 = require("app/actionCreators/modal");
const constants_1 = require("app/constants");
const modalStore_1 = (0, tslib_1.__importDefault)(require("app/stores/modalStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getModalPortal_1 = (0, tslib_1.__importDefault)(require("app/utils/getModalPortal"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const components_1 = require("./components");
function GlobalModal({ visible = false, options = {}, children, onClose }) {
    var _a, _b;
    const closeModal = React.useCallback(() => {
        var _a;
        // Option close callback, from the thing which opened the modal
        (_a = options.onClose) === null || _a === void 0 ? void 0 : _a.call(options);
        // Action creator, actually closes the modal
        (0, modal_1.closeModal)();
        // GlobalModal onClose prop callback
        onClose === null || onClose === void 0 ? void 0 : onClose();
    }, [options]);
    const handleEscapeClose = React.useCallback((e) => e.key === 'Escape' && closeModal(), [closeModal]);
    const portal = (0, getModalPortal_1.default)();
    const focusTrap = React.useRef();
    // SentryApp might be missing on tests
    if (window.SentryApp) {
        window.SentryApp.modalFocusTrap = focusTrap;
    }
    React.useEffect(() => {
        focusTrap.current = (0, focus_trap_1.createFocusTrap)(portal, {
            preventScroll: true,
            escapeDeactivates: false,
            fallbackFocus: portal,
        });
    }, [portal]);
    React.useEffect(() => {
        var _a;
        const body = document.querySelector('body');
        const root = document.getElementById(constants_1.ROOT_ELEMENT);
        if (!body || !root) {
            return () => void 0;
        }
        const reset = () => {
            var _a;
            body.style.removeProperty('overflow');
            root.removeAttribute('aria-hidden');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.deactivate();
            portal.removeEventListener('keydown', handleEscapeClose);
        };
        if (visible) {
            body.style.overflow = 'hidden';
            root.setAttribute('aria-hidden', 'true');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.activate();
            portal.addEventListener('keydown', handleEscapeClose);
        }
        else {
            reset();
        }
        return reset;
    }, [portal, handleEscapeClose, visible]);
    // Close the modal when the browser history changes
    React.useEffect(() => react_router_1.browserHistory.listen(() => (0, modal_1.closeModal)()), []);
    const renderedChild = children === null || children === void 0 ? void 0 : children({
        CloseButton: (0, components_1.makeCloseButton)(closeModal),
        Header: (0, components_1.makeClosableHeader)(closeModal),
        Body: components_1.ModalBody,
        Footer: components_1.ModalFooter,
        closeModal,
    });
    // Default to enabled backdrop
    const backdrop = (_a = options.backdrop) !== null && _a !== void 0 ? _a : true;
    // Default to enabled click close
    const allowClickClose = (_b = options.allowClickClose) !== null && _b !== void 0 ? _b : true;
    // Only close when we directly click outside of the modal.
    const containerRef = React.useRef(null);
    const clickClose = (e) => containerRef.current === e.target && allowClickClose && closeModal();
    return react_dom_1.default.createPortal(<React.Fragment>
      <Backdrop style={backdrop && visible ? { opacity: 0.5, pointerEvents: 'auto' } : {}}/>
      <Container ref={containerRef} style={{ pointerEvents: visible ? 'auto' : 'none' }} onClick={backdrop === true ? clickClose : undefined}>
        <framer_motion_1.AnimatePresence>
          {visible && (<Modal role="dialog" css={options.modalCss}>
              <Content role="document">{renderedChild}</Content>
            </Modal>)}
        </framer_motion_1.AnimatePresence>
      </Container>
    </React.Fragment>, portal);
}
const fullPageCss = (0, react_1.css) `
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
`;
const Backdrop = (0, styled_1.default)('div') `
  ${fullPageCss};
  z-index: ${p => p.theme.zIndex.modal};
  background: ${p => p.theme.gray500};
  will-change: opacity;
  transition: opacity 200ms;
  pointer-events: none;
  opacity: 0;
`;
const Container = (0, styled_1.default)('div') `
  ${fullPageCss};
  z-index: ${p => p.theme.zIndex.modal};
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow-y: auto;
`;
const Modal = (0, styled_1.default)(framer_motion_1.motion.div) `
  width: 640px;
  pointer-events: auto;
  padding: 80px ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(2)};
`;
Modal.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 15 },
    transition: (0, testableTransition_1.default)({
        opacity: { duration: 0.2 },
        y: { duration: 0.25 },
    }),
};
const Content = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(4)};
  background: ${p => p.theme.background};
  border-radius: 8px;
  border: ${p => p.theme.modalBorder};
  box-shadow: ${p => p.theme.modalBoxShadow};
`;
class GlobalModalContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            modalStore: modalStore_1.default.get(),
        };
        this.unlistener = modalStore_1.default.listen((modalStore) => this.setState({ modalStore }), undefined);
    }
    componentWillUnmount() {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    render() {
        const { modalStore } = this.state;
        const visible = !!modalStore && typeof modalStore.renderer === 'function';
        return (<GlobalModal {...this.props} {...modalStore} visible={visible}>
        {visible ? modalStore.renderer : null}
      </GlobalModal>);
    }
}
exports.default = GlobalModalContainer;
//# sourceMappingURL=index.jsx.map