/*
 * 저장한 글·사례 (2026-11-02)
 * 로그인 없이 이 브라우저의 localStorage에만 둔다. 저장소를 못 쓰는 환경(사생활 보호
 * 모드 등)에서는 조용히 빈 목록으로 동작한다.
 */

export type SavedKind = "post" | "case";

export type SavedItem = {
  id: string;
  kind: SavedKind;
  title: string;
  url: string;
  meta?: string;
  savedAt: number;
};

const KEY = "fal-saved-v1";
const EVENT = "fal:saved-change";

export function getSaved(): SavedItem[] {
  try {
    const raw = localStorage.getItem(KEY);
    const list = raw ? (JSON.parse(raw) as SavedItem[]) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function write(list: SavedItem[]) {
  try {
    localStorage.setItem(KEY, JSON.stringify(list));
  } catch {
    // 저장이 막혀 있으면 이번 화면에서만 반영된다.
  }
  document.dispatchEvent(new CustomEvent(EVENT));
}

export const isSaved = (id: string) => getSaved().some(it => it.id === id);

export function toggleSaved(item: Omit<SavedItem, "savedAt">): boolean {
  const list = getSaved();
  if (list.some(it => it.id === item.id)) {
    write(list.filter(it => it.id !== item.id));
    return false;
  }
  write([{ ...item, savedAt: Date.now() }, ...list]);
  return true;
}

export function removeSaved(id: string) {
  write(getSaved().filter(it => it.id !== id));
}

/** 이 탭과 다른 탭의 변경을 모두 알려준다. 돌려받은 함수로 구독을 끊는다. */
export function onSavedChange(cb: () => void): () => void {
  const onStorage = (e: StorageEvent) => e.key === KEY && cb();
  document.addEventListener(EVENT, cb);
  window.addEventListener("storage", onStorage);
  return () => {
    document.removeEventListener(EVENT, cb);
    window.removeEventListener("storage", onStorage);
  };
}
