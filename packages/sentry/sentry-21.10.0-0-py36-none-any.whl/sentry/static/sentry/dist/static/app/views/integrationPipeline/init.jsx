Object.defineProperty(exports, "__esModule", { value: true });
exports.init = void 0;
require("focus-visible");
const initializePipelineView_1 = require("app/bootstrap/initializePipelineView");
function init() {
    (0, initializePipelineView_1.initializePipelineView)(window.__initialData);
}
exports.init = init;
//# sourceMappingURL=init.jsx.map