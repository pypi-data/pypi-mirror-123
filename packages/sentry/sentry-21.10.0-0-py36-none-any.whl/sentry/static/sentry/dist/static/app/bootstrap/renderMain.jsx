Object.defineProperty(exports, "__esModule", { value: true });
exports.renderMain = void 0;
const tslib_1 = require("tslib");
const constants_1 = require("app/constants");
const main_1 = (0, tslib_1.__importDefault)(require("app/main"));
const renderDom_1 = require("./renderDom");
function renderMain() {
    try {
        (0, renderDom_1.renderDom)(main_1.default, `#${constants_1.ROOT_ELEMENT}`);
    }
    catch (err) {
        if (err.message === 'URI malformed') {
            // eslint-disable-next-line no-console
            console.error(new Error('An unencoded "%" has appeared, it is super effective! (See https://github.com/ReactTraining/history/issues/505)'));
            window.location.assign(window.location.pathname);
        }
    }
}
exports.renderMain = renderMain;
//# sourceMappingURL=renderMain.jsx.map