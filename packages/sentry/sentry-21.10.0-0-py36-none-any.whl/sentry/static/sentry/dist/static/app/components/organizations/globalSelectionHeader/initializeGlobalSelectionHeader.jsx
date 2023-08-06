Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const globalSelection_1 = require("app/actionCreators/globalSelection");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const utils_1 = require("./utils");
const getDateObjectFromQuery = query => Object.fromEntries(Object.entries(query).filter(([key]) => globalSelectionHeader_1.DATE_TIME_KEYS.includes(key)));
/**
 * Initializes GlobalSelectionHeader
 *
 * Calls an actionCreator to load project/environment from local storage if possible,
 * otherwise populate with defaults.
 *
 * This should only happen when the header is mounted
 * e.g. when changing views or organizations.
 */
class InitializeGlobalSelectionHeader extends React.Component {
    componentDidMount() {
        const { location, router, organization, defaultSelection, forceProject, memberProjects, shouldForceProject, shouldEnforceSingleProject, skipLoadLastUsed, showAbsolute, } = this.props;
        (0, globalSelection_1.initializeUrlState)({
            organization,
            queryParams: location.query,
            router,
            skipLoadLastUsed,
            memberProjects,
            defaultSelection,
            forceProject,
            shouldForceProject,
            shouldEnforceSingleProject,
            showAbsolute,
        });
    }
    componentDidUpdate(prevProps) {
        /**
         * This happens e.g. using browser's navigation button, in which case
         * we need to update our store to reflect URL changes
         */
        if (prevProps.location.query !== this.props.location.query) {
            const oldQuery = (0, utils_1.getStateFromQuery)(prevProps.location.query, {
                allowEmptyPeriod: true,
            });
            const newQuery = (0, utils_1.getStateFromQuery)(this.props.location.query, {
                allowEmptyPeriod: true,
            });
            const newEnvironments = newQuery.environment || [];
            const newDateObject = getDateObjectFromQuery(newQuery);
            const oldDateObject = getDateObjectFromQuery(oldQuery);
            /**
             * Do not pass router to these actionCreators, as we do not want to update
             * routes since these state changes are happening due to a change of routes
             */
            if (!(0, isEqual_1.default)(oldQuery.project, newQuery.project)) {
                (0, globalSelection_1.updateProjects)(newQuery.project || [], null, { environments: newEnvironments });
            }
            else if (!(0, isEqual_1.default)(oldQuery.environment, newQuery.environment)) {
                /**
                 * When the project stays the same, it's still possible that the environment
                 * changed, so explictly update the enviornment
                 */
                (0, globalSelection_1.updateEnvironments)(newEnvironments);
            }
            if (!(0, isEqual_1.default)(oldDateObject, newDateObject)) {
                (0, globalSelection_1.updateDateTime)(newDateObject);
            }
        }
    }
    render() {
        return null;
    }
}
exports.default = InitializeGlobalSelectionHeader;
//# sourceMappingURL=initializeGlobalSelectionHeader.jsx.map