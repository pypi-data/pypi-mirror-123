Object.defineProperty(exports, "__esModule", { value: true });
exports.openDashboardWidgetQuerySelectorModal = exports.demoSignupModal = exports.openReprocessEventModal = exports.openAddDashboardWidgetModal = exports.openInviteMembersModal = exports.openDebugFileSourceModal = exports.openHelpSearchModal = exports.redirectToProject = exports.openTeamAccessRequestModal = exports.openRecoveryOptions = exports.openCommandPalette = exports.openEditOwnershipRules = exports.openCreateOwnershipRule = exports.openCreateTeamModal = exports.openDiffModal = exports.openEmailVerification = exports.openSudo = exports.closeModal = exports.openModal = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const modalActions_1 = (0, tslib_1.__importDefault)(require("app/actions/modalActions"));
/**
 * Show a modal
 */
function openModal(renderer, options) {
    modalActions_1.default.openModal(renderer, options !== null && options !== void 0 ? options : {});
}
exports.openModal = openModal;
/**
 * Close modal
 */
function closeModal() {
    modalActions_1.default.closeModal();
}
exports.closeModal = closeModal;
function openSudo(_a = {}) {
    var { onClose } = _a, args = (0, tslib_1.__rest)(_a, ["onClose"]);
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/sudoModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...args}/>, { onClose });
    });
}
exports.openSudo = openSudo;
function openEmailVerification(_a = {}) {
    var { onClose } = _a, args = (0, tslib_1.__rest)(_a, ["onClose"]);
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/emailVerificationModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...args}/>, { onClose });
    });
}
exports.openEmailVerification = openEmailVerification;
function openDiffModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/diffModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { modalCss });
    });
}
exports.openDiffModal = openDiffModal;
function openCreateTeamModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/createTeamModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...options}/>);
    });
}
exports.openCreateTeamModal = openCreateTeamModal;
function openCreateOwnershipRule(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/createOwnershipRuleModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { modalCss });
    });
}
exports.openCreateOwnershipRule = openCreateOwnershipRule;
function openEditOwnershipRules(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/editOwnershipRulesModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { backdrop: 'static', modalCss });
    });
}
exports.openEditOwnershipRules = openEditOwnershipRules;
function openCommandPalette(options = {}) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/commandPalette')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { modalCss });
    });
}
exports.openCommandPalette = openCommandPalette;
function openRecoveryOptions(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/recoveryOptionsModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...options}/>);
    });
}
exports.openRecoveryOptions = openRecoveryOptions;
function openTeamAccessRequestModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/teamAccessRequestModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...options}/>);
    });
}
exports.openTeamAccessRequestModal = openTeamAccessRequestModal;
function redirectToProject(newProjectSlug) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/redirectToProject')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} slug={newProjectSlug}/>, {});
    });
}
exports.redirectToProject = redirectToProject;
function openHelpSearchModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/helpSearchModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { modalCss });
    });
}
exports.openHelpSearchModal = openHelpSearchModal;
function openDebugFileSourceModal(_a) {
    var { onClose } = _a, restOptions = (0, tslib_1.__rest)(_a, ["onClose"]);
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require(
        /* webpackChunkName: "DebugFileCustomRepository" */ 'app/components/modals/debugFileCustomRepository')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...restOptions}/>, {
            modalCss,
            onClose,
        });
    });
}
exports.openDebugFileSourceModal = openDebugFileSourceModal;
function openInviteMembersModal(_a = {}) {
    var { onClose } = _a, args = (0, tslib_1.__rest)(_a, ["onClose"]);
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/inviteMembersModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...args}/>, { modalCss, onClose });
    });
}
exports.openInviteMembersModal = openInviteMembersModal;
function openAddDashboardWidgetModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/addDashboardWidgetModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { backdrop: 'static', modalCss });
    });
}
exports.openAddDashboardWidgetModal = openAddDashboardWidgetModal;
function openReprocessEventModal(_a) {
    var { onClose } = _a, options = (0, tslib_1.__rest)(_a, ["onClose"]);
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/reprocessEventModal')));
        const { default: Modal } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { onClose });
    });
}
exports.openReprocessEventModal = openReprocessEventModal;
function demoSignupModal(options = {}) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/demoSignUp')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { modalCss });
    });
}
exports.demoSignupModal = demoSignupModal;
function openDashboardWidgetQuerySelectorModal(options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/modals/dashboardWidgetQuerySelectorModal')));
        const { default: Modal, modalCss } = mod;
        openModal(deps => <Modal {...deps} {...options}/>, { backdrop: 'static', modalCss });
    });
}
exports.openDashboardWidgetQuerySelectorModal = openDashboardWidgetQuerySelectorModal;
//# sourceMappingURL=modal.jsx.map