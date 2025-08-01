#include <gtk/gtk.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int priority;
    char *description;
} Task;

typedef struct {
    GList *tasks;
    GtkListStore *store;
    GtkWidget *treeview;
    GtkWidget *window;
} AppData;

static void free_task(Task *task) {
    if (task) {
        free(task->description);
        free(task);
    }
}

static void refresh_list(AppData *app) {
    gtk_list_store_clear(app->store);
    for (GList *l = app->tasks; l != NULL; l = l->next) {
        Task *t = (Task *)l->data;
        GtkTreeIter iter;
        gtk_list_store_append(app->store, &iter);
        gtk_list_store_set(app->store, &iter,
                           0, t->priority,
                           1, t->description,
                           -1);
    }
}

static void on_add_clicked(GtkButton *button, gpointer user_data) {
    AppData *app = (AppData *)user_data;
    GtkWidget *dialog = gtk_dialog_new_with_buttons("Ajouter une tâche", GTK_WINDOW(app->window),
                                                    GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                                    "_Ajouter", GTK_RESPONSE_ACCEPT,
                                                    "_Annuler", GTK_RESPONSE_REJECT,
                                                    NULL);
    GtkWidget *content_area = gtk_dialog_get_content_area(GTK_DIALOG(dialog));
    GtkWidget *grid = gtk_grid_new();
    gtk_grid_set_row_spacing(GTK_GRID(grid), 6);
    gtk_grid_set_column_spacing(GTK_GRID(grid), 6);

    GtkWidget *label_prio = gtk_label_new("Priorité (entier) :");
    GtkWidget *entry_prio = gtk_entry_new();
    GtkWidget *label_desc = gtk_label_new("Description :");
    GtkWidget *entry_desc = gtk_entry_new();

    gtk_grid_attach(GTK_GRID(grid), label_prio, 0, 0, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), entry_prio, 1, 0, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), label_desc, 0, 1, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), entry_desc, 1, 1, 1, 1);

    gtk_container_add(GTK_CONTAINER(content_area), grid);
    gtk_widget_show_all(dialog);

    int response = gtk_dialog_run(GTK_DIALOG(dialog));
    if (response == GTK_RESPONSE_ACCEPT) {
        const char *prio_str = gtk_entry_get_text(GTK_ENTRY(entry_prio));
        const char *desc_str = gtk_entry_get_text(GTK_ENTRY(entry_desc));
        if (prio_str && *prio_str && desc_str && *desc_str) {
            char *endptr;
            int prio = strtol(prio_str, &endptr, 10);
            if (*endptr == '\0') {
                Task *t = malloc(sizeof(Task));
                if (t) {
                    t->priority = prio;
                    t->description = strdup(desc_str);
                    app->tasks = g_list_append(app->tasks, t);
                    refresh_list(app);
                }
            }
        }
    }
    gtk_widget_destroy(dialog);
}

static void on_remove_clicked(GtkButton *button, gpointer user_data) {
    AppData *app = (AppData *)user_data;
    GtkTreeSelection *selection = gtk_tree_view_get_selection(GTK_TREE_VIEW(app->treeview));
    GtkTreeModel *model;
    GtkTreeIter iter;
    if (gtk_tree_selection_get_selected(selection, &model, &iter)) {
        int prio;
        char *desc;
        gtk_tree_model_get(model, &iter, 0, &prio, 1, &desc, -1);
        for (GList *l = app->tasks; l != NULL; l = l->next) {
            Task *t = (Task *)l->data;
            if (t->priority == prio && strcmp(t->description, desc) == 0) {
                app->tasks = g_list_remove(app->tasks, t);
                free_task(t);
                break;
            }
        }
        g_free(desc);
        refresh_list(app);
    }
}

static void activate(GtkApplication *app, gpointer user_data) {
    AppData *data = g_new0(AppData, 1);

    data->window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(data->window), "Gestionnaire de tâches");
    gtk_window_set_default_size(GTK_WINDOW(data->window), 400, 300);

    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_window_set_child(GTK_WINDOW(data->window), vbox);

    data->store = gtk_list_store_new(2, G_TYPE_INT, G_TYPE_STRING);

    data->treeview = gtk_tree_view_new_with_model(GTK_TREE_MODEL(data->store));
    GtkCellRenderer *renderer = gtk_cell_renderer_text_new();

    GtkTreeViewColumn *col_prio = gtk_tree_view_column_new_with_attributes("Priorité", renderer, "text", 0, NULL);
    gtk_tree_view_column_set_sort_column_id(col_prio, 0);
    GtkTreeViewColumn *col_desc = gtk_tree_view_column_new_with_attributes("Description", renderer, "text", 1, NULL);
    gtk_tree_view_column_set_sort_column_id(col_desc, 1);

    gtk_tree_view_append_column(GTK_TREE_VIEW(data->treeview), col_prio);
    gtk_tree_view_append_column(GTK_TREE_VIEW(data->treeview), col_desc);

    GtkWidget *scrolled = gtk_scrolled_window_new();
    gtk_scrolled_window_set_policy(GTK_SCROLLED_WINDOW(scrolled), GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);
    gtk_scrolled_window_set_child(GTK_SCROLLED_WINDOW(scrolled), data->treeview);

    gtk_box_append(GTK_BOX(vbox), scrolled);

    GtkWidget *hbox = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    GtkWidget *btn_add = gtk_button_new_with_label("Ajouter");
    GtkWidget *btn_remove = gtk_button_new_with_label("Supprimer");
    gtk_box_append(GTK_BOX(hbox), btn_add);
    gtk_box_append(GTK_BOX(hbox), btn_remove);
    gtk_box_append(GTK_BOX(vbox), hbox);

    g_signal_connect(btn_add, "clicked", G_CALLBACK(on_add_clicked), data);
    g_signal_connect(btn_remove, "clicked", G_CALLBACK(on_remove_clicked), data);

    gtk_widget_show(data->window);

    g_object_set_data_full(G_OBJECT(data->window), "appdata", data, (GDestroyNotify)g_free);
}

int main(int argc, char **argv) {
    GtkApplication *app = gtk_application_new("org.example.taskmanager", G_APPLICATION_FLAGS_NONE);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
