Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const intersection_1 = (0, tslib_1.__importDefault)(require("lodash/intersection"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const xor_1 = (0, tslib_1.__importDefault)(require("lodash/xor"));
const bulkNotice_1 = (0, tslib_1.__importDefault)(require("./bulkNotice"));
class BulkController extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.handleRowToggle = (id) => {
            this.setState(state => ({
                selectedIds: (0, xor_1.default)(state.selectedIds, [id]),
                isAllSelected: false,
            }));
        };
        this.handleAllRowsToggle = (select) => {
            const { pageIds } = this.props;
            this.setState({
                selectedIds: select ? [...pageIds] : [],
                isAllSelected: select,
            });
        };
        this.handlePageRowsToggle = (select) => {
            const { pageIds } = this.props;
            this.setState(state => ({
                selectedIds: select
                    ? (0, uniq_1.default)([...state.selectedIds, ...pageIds])
                    : state.selectedIds.filter(id => !pageIds.includes(id)),
                isAllSelected: false,
            }));
        };
    }
    getInitialState() {
        const { defaultSelectedIds, pageIds } = this.props;
        return {
            selectedIds: (0, intersection_1.default)(defaultSelectedIds !== null && defaultSelectedIds !== void 0 ? defaultSelectedIds : [], pageIds),
            isAllSelected: false,
        };
    }
    static getDerivedStateFromProps(props, state) {
        return Object.assign(Object.assign({}, state), { selectedIds: (0, intersection_1.default)(state.selectedIds, props.pageIds) });
    }
    componentDidUpdate(_prevProps, prevState) {
        var _a, _b;
        if (!(0, isEqual_1.default)(prevState, this.state)) {
            (_b = (_a = this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, this.state);
        }
    }
    render() {
        const { pageIds, children, columnsCount, allRowsCount, bulkLimit } = this.props;
        const { selectedIds, isAllSelected } = this.state;
        const isPageSelected = pageIds.length > 0 && pageIds.every(id => selectedIds.includes(id));
        const renderProps = {
            selectedIds,
            isAllSelected,
            isPageSelected,
            onRowToggle: this.handleRowToggle,
            onAllRowsToggle: this.handleAllRowsToggle,
            onPageRowsToggle: this.handlePageRowsToggle,
            renderBulkNotice: () => (<bulkNotice_1.default allRowsCount={allRowsCount} selectedRowsCount={selectedIds.length} onUnselectAllRows={() => this.handleAllRowsToggle(false)} onSelectAllRows={() => this.handleAllRowsToggle(true)} columnsCount={columnsCount} isPageSelected={isPageSelected} isAllSelected={isAllSelected} bulkLimit={bulkLimit}/>),
        };
        return children(renderProps);
    }
}
exports.default = BulkController;
//# sourceMappingURL=index.jsx.map