import numpy as np
from sklearn.tree import DecisionTreeClassifier
from collections import Counter

class SimpleRandomForest:
    def __init__(self, n_estimators=200, max_features="sqrt", max_depth=None, oob_score=False, random_state=42):
        # Guarda hiperparámetros
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.max_depth = max_depth
        self.oob_score = oob_score
        self.random_state = random_state
        # Inicializa estado
        self.trees_ = []
        self.feat_idx_ = []
        self.classes_ = None
        self.oob_score_ = None
        self._rng = np.random.default_rng(random_state)

    def _bootstrap_sample(self, X, y):
        # Toma muestra con reemplazo
        n = X.shape[0]
        idx = self._rng.integers(0, n, size=n)
        if self.oob_score:
            # Calcula índices fuera de bolsa
            all_idx = np.arange(n)
            mask = np.ones(n, dtype=bool)
            mask[idx] = False
            oob_idx = all_idx[mask]
            return X[idx], y[idx], oob_idx
        return X[idx], y[idx], None

    def _feature_subset(self, p):
        # Selecciona subconjunto de variables para el árbol
        if self.max_features == "sqrt":
            k = max(1, int(np.sqrt(p)))
        elif self.max_features in ("all", None):
            k = p
        elif isinstance(self.max_features, float):
            k = max(1, int(round(self.max_features * p)))
        elif isinstance(self.max_features, int):
            k = min(p, max(1, self.max_features))
        else:
            k = p
        return np.sort(self._rng.choice(p, size=k, replace=False))

    def fit(self, X, y):
        # Ajusta el ensamble con bootstrap y submuestreo de variables
        X = np.asarray(X)
        y = np.ravel(np.asarray(y))
        n, p = X.shape

        self.trees_.clear()
        self.feat_idx_.clear()
        self.oob_score_ = None

        # Guarda clases
        self.classes_ = np.unique(y)

        # Prepara semillas y acumuladores OOB
        seeds = self._rng.integers(0, 10_000_000, size=self.n_estimators)
        if self.oob_score:
            oob_sum = {}
            oob_cnt = {}

        for s in seeds:
            Xb, yb, oob_idx = self._bootstrap_sample(X, y)
            feats = self._feature_subset(p)

            tree = DecisionTreeClassifier(max_depth=self.max_depth, random_state=int(s))
            tree.fit(Xb[:, feats], yb)

            self.trees_.append(tree)
            self.feat_idx_.append(feats)

            # Acumula predicciones OOB
            if self.oob_score and oob_idx.size > 0:
                proba = tree.predict_proba(X[oob_idx][:, feats])
                for i, idx in enumerate(oob_idx):
                    if idx not in oob_sum:
                        oob_sum[idx] = proba[i].copy()
                        oob_cnt[idx] = 1
                    else:
                        oob_sum[idx] += proba[i]
                        oob_cnt[idx] += 1

        # Calcula métrica OOB
        if self.oob_score and len(oob_cnt) > 0:
            idxs = np.array(list(oob_cnt.keys()))
            proba = np.vstack([oob_sum[i] / oob_cnt[i] for i in idxs])
            y_hat = self.classes_[np.argmax(proba, axis=1)]
            self.oob_score_ = float(np.mean(y[idxs] == y_hat))

        return self

    def predict_proba(self, X):
        # Calcula probas promedio del ensamble
        if not self.trees_:
            raise ValueError("El modelo no está ajustado.")
        X = np.asarray(X)
        proba = None
        for t, f in zip(self.trees_, self.feat_idx_):
            p = t.predict_proba(X[:, f])
            proba = p if proba is None else (proba + p)
        proba /= len(self.trees_)
        return proba

    def predict(self, X):
        # Aplica voto duro con desempate por promedios de probas
        if not self.trees_:
            raise ValueError("El modelo no está ajustado.")
        X = np.asarray(X)

        preds = [t.predict(X[:, f]) for t, f in zip(self.trees_, self.feat_idx_)]
        votes = np.vstack(preds).T

        hard = np.array([Counter(row).most_common(1)[0][0] for row in votes])

        # Detecta empates y desempata con voto blando
        ties = []
        for row in votes:
            c = Counter(row)
            top = c.most_common(1)[0][1]
            ties.append(sum(v == top for v in c.values()) > 1)
        ties = np.array(ties, dtype=bool)

        if np.any(ties):
            soft = self.classes_[np.argmax(self.predict_proba(X[ties]), axis=1)]
            hard[ties] = soft

        return hard
