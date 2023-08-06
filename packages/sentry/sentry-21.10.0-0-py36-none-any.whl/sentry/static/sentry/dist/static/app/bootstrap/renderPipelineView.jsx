Object.defineProperty(exports, "__esModule", { value: true });
exports.renderPipelineView = void 0;
const tslib_1 = require("tslib");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const constants_1 = require("app/constants");
const pipelineView_1 = (0, tslib_1.__importDefault)(require("app/views/integrationPipeline/pipelineView"));
function render(pipelineName, props) {
    const rootEl = document.getElementById(constants_1.ROOT_ELEMENT);
    react_dom_1.default.render(<pipelineView_1.default pipelineName={pipelineName} {...props}/>, rootEl);
}
function renderPipelineView() {
    const { name, props } = window.__pipelineInitialData;
    render(name, props);
}
exports.renderPipelineView = renderPipelineView;
//# sourceMappingURL=renderPipelineView.jsx.map