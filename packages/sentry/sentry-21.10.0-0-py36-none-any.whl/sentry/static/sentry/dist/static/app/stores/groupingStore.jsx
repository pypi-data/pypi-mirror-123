Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const group_1 = require("app/actionCreators/group");
const indicator_1 = require("app/actionCreators/indicator");
const groupingActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupingActions"));
const api_1 = require("app/api");
// Between 0-100
const MIN_SCORE = 0.6;
// @param score: {[key: string]: number}
const checkBelowThreshold = (scores = {}) => {
    const scoreKeys = Object.keys(scores);
    return !scoreKeys.map(key => scores[key]).find(score => score >= MIN_SCORE);
};
const storeConfig = {
    listenables: [groupingActions_1.default],
    api: new api_1.Client(),
    init() {
        const state = this.getInitialState();
        Object.entries(state).forEach(([key, value]) => {
            this[key] = value;
        });
    },
    getInitialState() {
        return {
            // List of fingerprints that belong to issue
            mergedItems: [],
            // Map of {[fingerprint]: Array<fingerprint, event id>} that is selected to be unmerged
            unmergeList: new Map(),
            // Map of state for each fingerprint (i.e. "collapsed")
            unmergeState: new Map(),
            // Disabled state of "Unmerge" button in "Merged" tab (for Issues)
            unmergeDisabled: true,
            // If "Collapse All" was just used, this will be true
            unmergeLastCollapsed: false,
            // "Compare" button state
            enableFingerprintCompare: false,
            similarItems: [],
            filteredSimilarItems: [],
            similarLinks: '',
            mergeState: new Map(),
            mergeList: [],
            mergedLinks: '',
            mergeDisabled: false,
            loading: true,
            error: false,
        };
    },
    setStateForId(map, idOrIds, newState) {
        const ids = Array.isArray(idOrIds) ? idOrIds : [idOrIds];
        return ids.map(id => {
            const state = (map.has(id) && map.get(id)) || {};
            const mergedState = Object.assign(Object.assign({}, state), newState);
            map.set(id, mergedState);
            return mergedState;
        });
    },
    isAllUnmergedSelected() {
        const lockedItems = Array.from(this.unmergeState.values()).filter(({ busy }) => busy) || [];
        return (this.unmergeList.size ===
            this.mergedItems.filter(({ latestEvent }) => !!latestEvent).length -
                lockedItems.length);
    },
    // Fetches data
    onFetch(toFetchArray) {
        const requests = toFetchArray || this.toFetchArray;
        // Reset state and trigger update
        this.init();
        this.triggerFetchState();
        const promises = requests.map(({ endpoint, queryParams, dataKey }) => new Promise((resolve, reject) => {
            this.api.request(endpoint, {
                method: 'GET',
                data: queryParams,
                success: (data, _, resp) => {
                    resolve({
                        dataKey,
                        data,
                        links: resp ? resp.getResponseHeader('Link') : null,
                    });
                },
                error: err => {
                    var _a;
                    const error = ((_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || true;
                    reject(error);
                },
            });
        }));
        const responseProcessors = {
            merged: items => {
                const newItemsMap = {};
                const newItems = [];
                items.forEach(item => {
                    if (!newItemsMap[item.id]) {
                        const newItem = Object.assign({ eventCount: 0, children: [] }, item);
                        // Check for locked items
                        this.setStateForId(this.unmergeState, item.id, {
                            busy: item.state === 'locked',
                        });
                        newItemsMap[item.id] = newItem;
                        newItems.push(newItem);
                    }
                    const newItem = newItemsMap[item.id];
                    const { childId, childLabel, eventCount, lastSeen, latestEvent } = item;
                    if (eventCount) {
                        newItem.eventCount += eventCount;
                    }
                    if (childId) {
                        newItem.children.push({
                            childId,
                            childLabel,
                            lastSeen,
                            latestEvent,
                            eventCount,
                        });
                    }
                });
                return newItems;
            },
            similar: ([issue, scoreMap]) => {
                // Hide items with a low scores
                const isBelowThreshold = checkBelowThreshold(scoreMap);
                // List of scores indexed by interface (i.e., exception and message)
                // Note: for v2, the interface is always "similarity". When v2 is
                // rolled out we can get rid of this grouping entirely.
                const scoresByInterface = Object.keys(scoreMap)
                    .map(scoreKey => [scoreKey, scoreMap[scoreKey]])
                    .reduce((acc, [scoreKey, score]) => {
                    // v1 layout: '<interface>:...'
                    const [interfaceName] = String(scoreKey).split(':');
                    if (!acc[interfaceName]) {
                        acc[interfaceName] = [];
                    }
                    acc[interfaceName].push([scoreKey, score]);
                    return acc;
                }, {});
                // Aggregate score by interface
                const aggregate = Object.keys(scoresByInterface)
                    .map(interfaceName => [interfaceName, scoresByInterface[interfaceName]])
                    .reduce((acc, [interfaceName, allScores]) => {
                    // `null` scores means feature was not present in both issues, do not
                    // include in aggregate
                    const scores = allScores.filter(([, score]) => score !== null);
                    const avg = scores.reduce((sum, [, score]) => sum + score, 0) / scores.length;
                    acc[interfaceName] = avg;
                    return acc;
                }, {});
                return {
                    issue,
                    score: scoreMap,
                    scoresByInterface,
                    aggregate,
                    isBelowThreshold,
                };
            },
        };
        if (toFetchArray) {
            this.toFetchArray = toFetchArray;
        }
        return Promise.all(promises).then(resultsArray => {
            resultsArray.forEach(({ dataKey, data, links }) => {
                const items = dataKey === 'similar'
                    ? data.map(responseProcessors[dataKey])
                    : responseProcessors[dataKey](data);
                this[`${dataKey}Items`] = items;
                this[`${dataKey}Links`] = links;
            });
            this.loading = false;
            this.error = false;
            this.triggerFetchState();
        }, () => {
            this.loading = false;
            this.error = true;
            this.triggerFetchState();
        });
    },
    // Toggle merge checkbox
    onToggleMerge(id) {
        let checked = false;
        // Don't do anything if item is busy
        const state = this.mergeState.has(id) ? this.mergeState.get(id) : undefined;
        if ((state === null || state === void 0 ? void 0 : state.busy) === true) {
            return;
        }
        if (this.mergeList.includes(id)) {
            this.mergeList = this.mergeList.filter(item => item !== id);
        }
        else {
            this.mergeList = [...this.mergeList, id];
            checked = true;
        }
        this.setStateForId(this.mergeState, id, {
            checked,
        });
        this.triggerMergeState();
    },
    // Toggle unmerge check box
    onToggleUnmerge([fingerprint, eventId]) {
        let checked = false;
        // Uncheck an item to unmerge
        const state = this.unmergeState.get(fingerprint);
        if ((state === null || state === void 0 ? void 0 : state.busy) === true) {
            return;
        }
        if (this.unmergeList.has(fingerprint)) {
            this.unmergeList.delete(fingerprint);
        }
        else {
            this.unmergeList.set(fingerprint, eventId);
            checked = true;
        }
        // Update "checked" state for row
        this.setStateForId(this.unmergeState, fingerprint, {
            checked,
        });
        // Unmerge should be disabled if 0 or all items are selected, or if there's
        // only one item to select
        this.unmergeDisabled =
            this.mergedItems.size <= 1 ||
                this.unmergeList.size === 0 ||
                this.isAllUnmergedSelected();
        this.enableFingerprintCompare = this.unmergeList.size === 2;
        this.triggerUnmergeState();
    },
    onUnmerge({ groupId, loadingMessage, successMessage, errorMessage }) {
        const ids = Array.from(this.unmergeList.keys());
        return new Promise((resolve, reject) => {
            if (this.isAllUnmergedSelected()) {
                reject(new Error('Not allowed to unmerge ALL events'));
                return;
            }
            // Disable unmerge button
            this.unmergeDisabled = true;
            // Disable rows
            this.setStateForId(this.unmergeState, ids, {
                checked: false,
                busy: true,
            });
            this.triggerUnmergeState();
            (0, indicator_1.addLoadingMessage)(loadingMessage);
            this.api.request(`/issues/${groupId}/hashes/`, {
                method: 'DELETE',
                query: {
                    id: ids,
                },
                success: () => {
                    (0, indicator_1.addSuccessMessage)(successMessage);
                    // Busy rows after successful Unmerge
                    this.setStateForId(this.unmergeState, ids, {
                        checked: false,
                        busy: true,
                    });
                    this.unmergeList.clear();
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)(errorMessage);
                    this.setStateForId(this.unmergeState, ids, {
                        checked: true,
                        busy: false,
                    });
                },
                complete: () => {
                    this.unmergeDisabled = false;
                    resolve(this.triggerUnmergeState());
                },
            });
        });
    },
    // For cross-project views, we need to pass projectId instead of
    // depending on router params (since we will only have orgId in that case)
    onMerge({ params, query, projectId }) {
        if (!params) {
            return undefined;
        }
        const ids = this.mergeList;
        this.mergeDisabled = true;
        this.setStateForId(this.mergeState, ids, {
            busy: true,
        });
        this.triggerMergeState();
        const promise = new Promise(resolve => {
            // Disable merge button
            const { orgId, groupId } = params;
            (0, group_1.mergeGroups)(this.api, {
                orgId,
                projectId: projectId || params.projectId,
                itemIds: [...ids, groupId],
                query,
            }, {
                success: data => {
                    var _a;
                    if ((_a = data === null || data === void 0 ? void 0 : data.merge) === null || _a === void 0 ? void 0 : _a.parent) {
                        this.trigger({
                            mergedParent: data.merge.parent,
                        });
                    }
                    // Hide rows after successful merge
                    this.setStateForId(this.mergeState, ids, {
                        checked: false,
                        busy: true,
                    });
                    this.mergeList = [];
                },
                error: () => {
                    this.setStateForId(this.mergeState, ids, {
                        checked: true,
                        busy: false,
                    });
                },
                complete: () => {
                    this.mergeDisabled = false;
                    resolve(this.triggerMergeState());
                },
            });
        });
        return promise;
    },
    // Toggle collapsed state of all fingerprints
    onToggleCollapseFingerprints() {
        this.setStateForId(this.unmergeState, this.mergedItems.map(({ id }) => id), {
            collapsed: !this.unmergeLastCollapsed,
        });
        this.unmergeLastCollapsed = !this.unmergeLastCollapsed;
        this.trigger({
            unmergeLastCollapsed: this.unmergeLastCollapsed,
            unmergeState: this.unmergeState,
        });
    },
    onToggleCollapseFingerprint(fingerprint) {
        const collapsed = this.unmergeState.has(fingerprint) && this.unmergeState.get(fingerprint).collapsed;
        this.setStateForId(this.unmergeState, fingerprint, { collapsed: !collapsed });
        this.trigger({
            unmergeState: this.unmergeState,
        });
    },
    triggerFetchState() {
        const state = Object.assign({ similarItems: this.similarItems.filter(({ isBelowThreshold }) => !isBelowThreshold), filteredSimilarItems: this.similarItems.filter(({ isBelowThreshold }) => isBelowThreshold) }, (0, pick_1.default)(this, [
            'mergedItems',
            'mergedLinks',
            'similarLinks',
            'mergeState',
            'unmergeState',
            'loading',
            'error',
            'enableFingerprintCompare',
            'unmergeList',
        ]));
        this.trigger(state);
        return state;
    },
    triggerUnmergeState() {
        const state = (0, pick_1.default)(this, [
            'unmergeDisabled',
            'unmergeState',
            'unmergeList',
            'enableFingerprintCompare',
            'unmergeLastCollapsed',
        ]);
        this.trigger(state);
        return state;
    },
    triggerMergeState() {
        const state = (0, pick_1.default)(this, ['mergeDisabled', 'mergeState', 'mergeList']);
        this.trigger(state);
        return state;
    },
};
const GroupingStore = reflux_1.default.createStore(storeConfig);
exports.default = GroupingStore;
//# sourceMappingURL=groupingStore.jsx.map