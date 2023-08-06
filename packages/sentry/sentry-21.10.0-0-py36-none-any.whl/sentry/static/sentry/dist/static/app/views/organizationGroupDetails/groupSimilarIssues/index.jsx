Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const similarStackTrace_1 = (0, tslib_1.__importDefault)(require("./similarStackTrace"));
const GroupSimilarIssues = (_a) => {
    var { project } = _a, props = (0, tslib_1.__rest)(_a, ["project"]);
    return (<feature_1.default features={['similarity-view']} project={project}>
    <similarStackTrace_1.default project={project} {...props}/>
  </feature_1.default>);
};
exports.default = GroupSimilarIssues;
//# sourceMappingURL=index.jsx.map