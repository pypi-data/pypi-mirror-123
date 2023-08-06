Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const debugImage_1 = require("app/types/debugImage");
const utils_1 = require("../utils");
function Features({ download }) {
    let features = [];
    if (download.status === debugImage_1.CandidateDownloadStatus.OK ||
        download.status === debugImage_1.CandidateDownloadStatus.DELETED ||
        download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED) {
        features = Object.keys(download.features).filter(feature => download.features[feature]);
    }
    return (<react_1.Fragment>
      {Object.keys(debugImage_1.ImageFeature).map(imageFeature => {
            const { label, description } = (0, utils_1.getImageFeatureDescription)(imageFeature);
            const isDisabled = !features.includes(imageFeature);
            return (<StyledTag key={label} disabled={isDisabled} tooltipText={isDisabled ? undefined : description}>
            {label}
          </StyledTag>);
        })}
    </react_1.Fragment>);
}
exports.default = Features;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  opacity: ${p => (p.disabled ? '0.35' : 1)};
`;
//# sourceMappingURL=features.jsx.map