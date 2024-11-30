import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/20/solid";
import clsx from "clsx";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  pageSize: number;
  onPageSizeChange: (size: number) => void;
  totalItems: number;
}

export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  pageSize,
  onPageSizeChange,
  totalItems,
}: PaginationProps) => {
  const safeTotalPages = Math.max(1, totalPages);
  const safeCurrentPage = Math.min(Math.max(1, currentPage), safeTotalPages);

  const getVisiblePages = () => {
    const delta = 2;
    const pages: number[] = [];
    let left = Math.max(1, safeCurrentPage - delta);
    let right = Math.min(safeTotalPages, safeCurrentPage + delta);

    if (left > 1) {
      pages.push(1);
      if (left > 2) {
        pages.push(-1);
      }
    }

    for (let i = left; i <= right; i++) {
      pages.push(i);
    }

    if (right < safeTotalPages) {
      if (right < safeTotalPages - 1) {
        pages.push(-1);
      }
      pages.push(safeTotalPages);
    }

    return pages;
  };

  const pages = getVisiblePages();

  return (
    <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6">
      <div className="flex flex-1 justify-between sm:hidden">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className={clsx(
            "relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700",
            {
              "cursor-not-allowed opacity-50": currentPage === 1,
              "hover:bg-gray-50": currentPage !== 1,
            }
          )}
        >
          Назад
        </button>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className={clsx(
            "relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700",
            {
              "cursor-not-allowed opacity-50": currentPage === totalPages,
              "hover:bg-gray-50": currentPage !== totalPages,
            }
          )}
        >
          Вперед
        </button>
      </div>
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="rounded-md border-gray-300 py-1.5 text-base font-medium text-gray-700 focus:border-blue-500 focus:outline-none focus:ring-blue-500"
          >
            {[10, 20, 30, 50].map((size) => (
              <option key={size} value={size}>
                {size} / стр.
              </option>
            ))}
          </select>
          <span className="ml-8 text-sm text-gray-700">
            Всего: <span className="font-medium">{totalItems}</span> записей
          </span>
        </div>
        <div>
          <nav
            className="isolate inline-flex -space-x-px rounded-md shadow-sm"
            aria-label="Pagination"
          >
            <button
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            >
              <span className="sr-only">Предыдущая</span>
              <ChevronLeftIcon className="h-5 w-5" aria-hidden="true" />
            </button>
            {pages.map((page, index) => {
              if (page === -1) {
                return (
                  <span
                    key={`ellipsis-${index}`}
                    className="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
                  >
                    ...
                  </span>
                );
              }

              return (
                <button
                  key={page}
                  onClick={() => onPageChange(page)}
                  className={clsx(
                    "relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0",
                    {
                      "bg-blue-600 text-white focus:z-20": currentPage === page,
                      "text-gray-900 hover:bg-gray-50": currentPage !== page,
                    }
                  )}
                >
                  {page}
                </button>
              );
            })}
            <button
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            >
              <span className="sr-only">Следующая</span>
              <ChevronRightIcon className="h-5 w-5" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
};
