Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const getModalPortal = (0, memoize_1.default)(() => {
    let portal = document.getElementById('modal-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'modal-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
exports.default = getModalPortal;
//# sourceMappingURL=getModalPortal.jsx.map